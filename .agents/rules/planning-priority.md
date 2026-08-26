# Planning Priority Rules

> Scope: Agent workflow discipline — planning before building.

## Rules

1. **Never build during planning** — While the user is discussing requirements,
   architecture, design, or task breakdown, do not write any implementation
   code, scaffolding, or configuration files. Stay in discussion mode until the
   user explicitly signals that planning is complete and it's time to build.

2. **Wait for a clear "go" signal** — Do not assume planning is over. Wait for
   an explicit directive such as "let's start implementing", "let's build it",
   "start coding", or equivalent. If unsure, ask: *"Are you ready for me to
   start building?"*

3. **Planning output is research-only** — During planning you may:
   - Read existing code to understand the codebase.
   - Search for files and grep for references.
   - Ask clarifying questions.
   - Propose approaches in markdown/text.
   - Create todo lists to track planned work.
   
   You may **not**:
   - Create new source files.
   - Edit existing source/module files.
   - Install dependencies or run build commands.
   - Generate scaffolding or boilerplate.

4. **Respect the planning session** — If the user is reviewing options,
   weighing trade-offs, or asking for recommendations, treat that as a planning
   activity. Do not shortcut the conversation by jumping into code.

5. **Push back on premature builds** — If the user's request is ambiguous
   about whether it's planning or building, ask for clarification rather than
   defaulting to implementation. It's better to confirm intent than to undo
   work.

6. **Separate concerns in communication** — When asked for a plan, present it
   as a plan (design doc, checklist, architecture sketch) and keep it distinct
   from code. If the user then says "implement that", the context switch to
   building is explicit and intentional.