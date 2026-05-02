from __future__ import annotations

import json
import os
import re
import subprocess
from urllib import error, request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


LOCAL_AGENT_DIR = Path(__file__).resolve().parent.parent
WORKSPACE = LOCAL_AGENT_DIR.parent.parent
ROADMAP_PATH = WORKSPACE / "genai-roadmap.md"
PROJECTS_DIR = WORKSPACE / "projects"
DEFAULT_PROGRESS_PATH = LOCAL_AGENT_DIR / "roadmap-progress.local.json"
EXAMPLE_PROGRESS_PATH = LOCAL_AGENT_DIR / "roadmap-progress.example.json"
LOCAL_MODEL_BASE_URL = os.getenv(
    "LOCAL_MODEL_BASE_URL",
    os.getenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234"),
).rstrip("/")
LOCAL_MODEL_NAME = os.getenv("LOCAL_MODEL_NAME", "").strip()


@dataclass(frozen=True)
class Phase:
    id: int
    title: str
    body: str
    projects: list[str]


def load_progress(progress_path: Path = DEFAULT_PROGRESS_PATH) -> dict[str, Any]:
    if not progress_path.exists():
        return {
            "available": False,
            "message": (
                "No local progress file found. Create one with: "
                f"cp {EXAMPLE_PROGRESS_PATH.relative_to(WORKSPACE)} "
                f"{DEFAULT_PROGRESS_PATH.relative_to(WORKSPACE)}"
            ),
            "current_phase": None,
            "current_project": None,
            "completed_projects": [],
            "focus": "finish roadmap first",
            "notes": [],
        }

    with progress_path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)

    return {
        "available": True,
        "message": "Loaded local progress file.",
        "current_phase": _as_optional_int(raw.get("current_phase")),
        "current_project": _as_optional_str(raw.get("current_project")),
        "completed_projects": _as_str_list(raw.get("completed_projects")),
        "focus": _as_optional_str(raw.get("focus")) or "finish roadmap first",
        "notes": _as_str_list(raw.get("notes")),
    }


def parse_phases(roadmap_path: Path = ROADMAP_PATH) -> list[Phase]:
    text = roadmap_path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^# PHASE\s+(\d+)\s+-\s+(.+?)\s*$", text, re.MULTILINE))
    phases: list[Phase] = []

    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        projects = [
            item.strip()
            for item in re.findall(r"^#{3,4}\s+Project\s+\d+:\s+(.+?)\s*$", body, re.MULTILINE)
        ]
        phases.append(
            Phase(
                id=int(match.group(1)),
                title=match.group(2).strip(),
                body=body,
                projects=projects,
            )
        )

    return phases


def get_status(progress_path: Path = DEFAULT_PROGRESS_PATH) -> dict[str, Any]:
    progress = load_progress(progress_path)
    phases = parse_phases()
    detected_projects = detect_project_dirs()

    return {
        "focus": progress["focus"],
        "progress_available": progress["available"],
        "progress_message": progress["message"],
        "current_phase": progress["current_phase"],
        "current_project": progress["current_project"],
        "completed_projects": progress["completed_projects"],
        "notes": progress["notes"],
        "phase_count": len(phases),
        "detected_projects": detected_projects,
        "git": git_status_summary(),
    }


def get_phase_details(phase_id: int) -> dict[str, Any]:
    phase = _find_phase(phase_id)
    compact_body = _compact_text(phase.body, max_lines=55)
    return {
        "phase_id": phase.id,
        "title": phase.title,
        "projects": phase.projects,
        "summary": compact_body,
    }


def next_task(progress_path: Path = DEFAULT_PROGRESS_PATH) -> dict[str, Any]:
    status = get_status(progress_path)
    phases = parse_phases()
    phase = _select_phase(status, phases)
    project = _select_project(status, phase)
    project_path = _project_path(project, status["detected_projects"])

    files_to_inspect = [
        "genai-roadmap.md",
        str(project_path.relative_to(WORKSPACE)) if project_path else "projects/",
    ]
    if project_path and (project_path / "README.md").exists():
        files_to_inspect.append(str((project_path / "README.md").relative_to(WORKSPACE)))

    return {
        "title": f"Continue Phase {phase.id}: {phase.title}",
        "progress_available": status["progress_available"],
        "progress_message": status["progress_message"],
        "current_phase": phase.id,
        "current_project": project,
        "why": (
            "This keeps the main goal tight: finish the GenAI roadmap first, while using "
            "the local-agent only as support instead of turning it into a separate detour."
        ),
        "files_to_inspect": _dedupe(files_to_inspect),
        "steps": [
            f"Read the Phase {phase.id} section and confirm the expected project outcome.",
            f"Open the current project folder for `{project}` and review its README/tests.",
            "Run the existing checks before changing anything so you know the baseline.",
            "Implement the smallest missing behavior needed for this project milestone.",
            "Run the checks again and update notes/progress manually when done.",
        ],
        "verification_commands": _verification_commands(project_path),
        "done_when": [
            "The project has a clear README or usage path.",
            "Relevant tests/checks pass locally.",
            "The next roadmap checkbox/progress note can be updated with confidence.",
        ],
        "git": status["git"],
    }


def coach_next_task(
    progress_path: Path = DEFAULT_PROGRESS_PATH,
    max_tokens: int = 1600,
    temperature: float = 0.2,
) -> dict[str, Any]:
    deterministic_task = next_task(progress_path)
    phase_details = get_phase_details(deterministic_task["current_phase"])
    project_context = _project_context(deterministic_task["current_project"])
    prompt = _coach_prompt(deterministic_task, phase_details, project_context)

    try:
        model_response = call_local_model(
            prompt=prompt,
            system_prompt=(
                "You are a local GenAI roadmap coach. Be practical, concise, and specific. "
                "Use the provided local repo facts only. Do not invent files or progress."
            ),
            max_tokens=max_tokens,
            temperature=temperature,
        )
        if not model_response["ok"]:
            raise RuntimeError(str(model_response.get("error", "local model call failed")))
        return {
            **deterministic_task,
            "coach_mode": "llm",
            "model": model_response["model"],
            "coach_response": _clean_coach_output(model_response["output"]),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            **deterministic_task,
            "coach_mode": "fallback",
            "model": None,
            "coach_error": str(exc),
            "coach_response": format_next_task(deterministic_task),
        }


def call_local_model(
    prompt: str,
    system_prompt: str,
    max_tokens: int = 900,
    temperature: float = 0.2,
    base_url: str = LOCAL_MODEL_BASE_URL,
    model_name: str = LOCAL_MODEL_NAME,
) -> dict[str, Any]:
    models = _http_json(f"{base_url}/v1/models", timeout=8)
    model_ids = [
        item["id"]
        for item in models.get("data", [])
        if isinstance(item, dict) and item.get("id")
    ]
    chat_model_ids = [
        model_id
        for model_id in model_ids
        if "embed" not in model_id.lower()
    ]
    if not chat_model_ids:
        return {"ok": False, "error": f"No chat model available at {base_url}."}

    selected_model = model_name or chat_model_ids[0]
    if selected_model not in chat_model_ids and not model_name:
        return {"ok": False, "error": f"No selectable chat model available at {base_url}."}
    payload = {
        "model": selected_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    data = _http_json(f"{base_url}/v1/chat/completions", payload=payload, timeout=90)
    message = data.get("choices", [{}])[0].get("message", {})
    content = message.get("content", "")
    if isinstance(content, list):
        content = "".join(item.get("text", "") for item in content if isinstance(item, dict))
    if not isinstance(content, str):
        content = str(content)

    if not content.strip():
        content = message.get("reasoning_content", "") or message.get("reasoning", "")
        if not isinstance(content, str):
            content = str(content)

    return {
        "ok": True,
        "base_url": base_url,
        "model": selected_model,
        "output": content,
        "finish_reason": data.get("choices", [{}])[0].get("finish_reason", ""),
    }


# Backward-compatible alias for older local tests/imports.
call_lm_studio = call_local_model


def detect_project_dirs() -> list[str]:
    if not PROJECTS_DIR.exists():
        return []
    return sorted(
        path.name
        for path in PROJECTS_DIR.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )


def git_status_summary() -> str:
    try:
        result = subprocess.run(
            ["git", "status", "--short", "--branch"],
            cwd=WORKSPACE,
            shell=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as exc:  # noqa: BLE001
        return f"git status unavailable: {exc}"

    output = (result.stdout + result.stderr).strip()
    return output or "Clean worktree"


def format_status(status: dict[str, Any]) -> str:
    lines = [
        "# Roadmap Coach Status",
        "",
        f"Focus: {status['focus']}",
        f"Progress: {status['progress_message']}",
        f"Current phase: {status['current_phase'] or 'unknown'}",
        f"Current project: {status['current_project'] or 'unknown'}",
        f"Completed projects: {_join_or_none(status['completed_projects'])}",
        f"Detected projects: {_join_or_none(status['detected_projects'])}",
        "",
        "## Git",
        status["git"],
    ]
    if status["notes"]:
        lines.extend(["", "## Notes", *[f"- {note}" for note in status["notes"]]])
    return "\n".join(lines)


def format_phase(details: dict[str, Any]) -> str:
    lines = [
        f"# Phase {details['phase_id']}: {details['title']}",
        "",
        "## Projects",
        *[f"- {project}" for project in details["projects"]],
        "",
        "## Roadmap Notes",
        details["summary"],
    ]
    return "\n".join(lines)


def format_next_task(task: dict[str, Any]) -> str:
    lines = [
        f"# {task['title']}",
        "",
        f"Project: {task['current_project']}",
        f"Progress: {task['progress_message']}",
        "",
        "## Why",
        task["why"],
        "",
        "## Files To Inspect",
        *[f"- {item}" for item in task["files_to_inspect"]],
        "",
        "## Steps",
        *[f"{index}. {step}" for index, step in enumerate(task["steps"], start=1)],
        "",
        "## Verification",
        *[f"- `{command}`" for command in task["verification_commands"]],
        "",
        "## Done When",
        *[f"- {item}" for item in task["done_when"]],
    ]
    return "\n".join(lines)


def format_coach_task(task: dict[str, Any]) -> str:
    if task.get("coach_mode") == "llm":
        return "\n".join(
            [
                f"# {task['title']}",
                "",
                f"Model: {task['model']}",
                "",
                task["coach_response"],
            ]
        )

    lines = [
        "# Local Model Unavailable",
        "",
        f"Reason: {task.get('coach_error', 'unknown error')}",
        "",
        "Falling back to deterministic roadmap plan:",
        "",
        task["coach_response"],
    ]
    return "\n".join(lines)


def _find_phase(phase_id: int) -> Phase:
    for phase in parse_phases():
        if phase.id == phase_id:
            return phase
    raise ValueError(f"Unknown phase id: {phase_id}")


def _select_phase(status: dict[str, Any], phases: list[Phase]) -> Phase:
    current_phase = status.get("current_phase")
    if isinstance(current_phase, int):
        for phase in phases:
            if phase.id == current_phase:
                return phase

    highest = _highest_project_prefix(status["detected_projects"])
    if highest is not None:
        inferred_phase_id = 1 if highest <= 3 else highest
        for phase in phases:
            if phase.id == inferred_phase_id:
                return phase

    return phases[0]


def _select_project(status: dict[str, Any], phase: Phase) -> str:
    current_project = status.get("current_project")
    if current_project:
        return str(current_project)

    detected = status["detected_projects"]
    highest_project = _highest_project_name(detected)
    if highest_project:
        return highest_project

    if phase.projects:
        return phase.projects[0]
    return f"phase-{phase.id}"


def _project_path(project: str, detected_projects: list[str]) -> Path | None:
    if project in detected_projects:
        return PROJECTS_DIR / project

    lowered = project.lower()
    for name in detected_projects:
        if name.lower() == lowered or lowered in name.lower() or name.lower() in lowered:
            return PROJECTS_DIR / name
    return None


def _verification_commands(project_path: Path | None) -> list[str]:
    if not project_path:
        return ["git status --short", "python -m pytest"]
    rel = project_path.relative_to(WORKSPACE)
    commands = ["git status --short"]
    if (project_path / "Makefile").exists():
        commands.append(f"cd {rel} && make test")
    elif (project_path / "pyproject.toml").exists():
        commands.append(f"cd {rel} && python -m pytest")
    else:
        commands.append(f"ls -la {rel}")
    return commands


def _highest_project_prefix(projects: list[str]) -> int | None:
    numbers = []
    for name in projects:
        match = re.match(r"p(\d+)-", name)
        if match and name != "p0-genai-starter-template":
            numbers.append(int(match.group(1)))
    return max(numbers) if numbers else None


def _highest_project_name(projects: list[str]) -> str | None:
    candidates: list[tuple[int, str]] = []
    for name in projects:
        match = re.match(r"p(\d+)-", name)
        if match and name != "p0-genai-starter-template":
            candidates.append((int(match.group(1)), name))
    if not candidates:
        return None
    return sorted(candidates)[-1][1]


def _compact_text(text: str, max_lines: int) -> str:
    useful_lines = []
    for line in text.splitlines():
        stripped = line.rstrip()
        if not stripped and (not useful_lines or not useful_lines[-1]):
            continue
        useful_lines.append(stripped)
        if len(useful_lines) >= max_lines:
            useful_lines.append("...[truncated]")
            break
    return "\n".join(useful_lines).strip()


def _project_context(project: str) -> dict[str, Any]:
    detected = detect_project_dirs()
    path = _project_path(project, detected)
    if not path:
        return {"path": None, "readme": "", "files": []}

    readme = ""
    readme_path = path / "README.md"
    if readme_path.exists():
        readme = _compact_text(readme_path.read_text(encoding="utf-8", errors="replace"), max_lines=25)

    files = []
    for child in sorted(path.rglob("*")):
        if child.is_file() and ".venv" not in child.parts and "__pycache__" not in child.parts:
            files.append(str(child.relative_to(WORKSPACE)))
        if len(files) >= 25:
            files.append("...[truncated]")
            break

    return {
        "path": str(path.relative_to(WORKSPACE)),
        "readme": readme,
        "files": files,
    }


def _coach_prompt(
    task: dict[str, Any],
    phase_details: dict[str, Any],
    project_context: dict[str, Any],
) -> str:
    files = ", ".join(project_context["files"][:12])
    return (
        "Coach the next roadmap action from these local repo facts only.\n"
        "Do not reveal hidden reasoning, analysis, or a thinking process.\n"
        "Return exactly five short sections: Next Move, Why This Matters, Steps, Checks, Done When.\n"
        "Keep it under 220 words.\n\n"
        f"Task: {task['title']}\n"
        f"Phase: {task['current_phase']} - {phase_details['title']}\n"
        f"Project: {task['current_project']}\n"
        f"Progress: {task['progress_message']}\n"
        f"Files to inspect: {', '.join(task['files_to_inspect'])}\n"
        f"Verification commands: {', '.join(task['verification_commands'])}\n"
        f"Project path: {project_context['path']}\n"
        f"Project files: {files}\n"
        f"Project README excerpt: {project_context['readme'][:650]}\n"
        f"Git status excerpt: {task['git'][:450]}\n"
    )


def _clean_coach_output(text: str) -> str:
    cleaned = text.strip()
    regex_markers = [
        r"\*\*\s*\d+\.\s*Next Move\s*\*\*",
        r"\*\*\s*Next Move\s*:\s*\*\*",
        r"\*\*\s*Next Move\s*\*\*",
        r"\*\s*Next Move\s*:\s*\*",
        r"#{1,3}\s*Next Move",
        r"(^|\n)\s*\d+\.\s*Next Move",
        r"(^|\n)\s*Next Move\s*:",
    ]
    latest_match: re.Match[str] | None = None
    for pattern in regex_markers:
        matches = list(re.finditer(pattern, cleaned, flags=re.IGNORECASE))
        if matches:
            candidate = matches[-1]
            if latest_match is None or candidate.start() > latest_match.start():
                latest_match = candidate
    if latest_match:
        return _trim_coach_meta(cleaned[latest_match.start():].strip())

    markers = [
        "\n# Next Move",
        "\n## Next Move",
        "\nNext Move",
        "Next Move\n",
        "**Next Move**",
    ]
    for marker in markers:
        index = cleaned.find(marker)
        if index >= 0:
            return cleaned[index:].strip()

    if "Thinking Process:" in cleaned:
        lines = []
        capture = False
        for line in cleaned.splitlines():
            stripped = line.strip()
            if stripped.strip("*: ").lower() == "next move":
                capture = True
            if capture:
                lines.append(line)
        if lines:
            return _trim_coach_meta("\n".join(lines).strip())

    return _trim_coach_meta(cleaned)


def _trim_coach_meta(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip().lower()
        if stripped.startswith("*word count") or stripped.startswith("*sections"):
            break
        lines.append(line)
    return "\n".join(lines).strip()


def _http_json(
    url: str,
    payload: dict[str, Any] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    try:
        if payload is None:
            with request.urlopen(url, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))

        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body}") from exc


def _as_optional_int(value: object) -> int | None:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return None


def _as_optional_str(value: object) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _as_str_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _join_or_none(items: list[str]) -> str:
    return ", ".join(items) if items else "none"


def _dedupe(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
