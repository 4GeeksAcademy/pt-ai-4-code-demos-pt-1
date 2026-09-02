# MDX Content Architecture

## Status

Accepted

## Context

The application is a small educational site whose article content should be reviewed, versioned, and deployed with source code. It requires React-enhanced MDX without introducing a CMS or exposing server-side runtime compilation to user-provided content. Article metadata must also be consistently available for listings, static routes, metadata, and a future Fuse.js search index.

## Decision

Use filesystem-backed MDX under `content/articles/`, compiled at build time through Next.js MDX support.

Parse YAML frontmatter in a server-only content module and validate it against a strict schema. Derive slugs from filenames, rather than allowing authors to specify them. The module returns normalized article records, including plain `searchText`, for every content consumer.

MDX is trusted repository content. Authors use a centrally defined MDX component map. Arbitrary imports from MDX files are not supported in the initial architecture.

## Consequences

### Positive

- Articles can be reviewed with their source code and deployed atomically.
- Pages and content metadata are statically generated with no runtime CMS dependency.
- Strict validation finds content errors during local builds and CI.
- A single normalized collection avoids divergent logic for routes, listings, and search.
- The curated component map provides an intentional and maintainable authoring API.

### Negative

- Publishing content requires a repository change and deployment.
- Build duration grows with the article collection.
- New rich content components require application development instead of ad hoc MDX imports.

## Alternatives Considered

### Headless CMS

Rejected for the initial release because it adds operational dependencies and separates content changes from the code review and deployment workflow.

### Runtime MDX Compilation

Rejected because the content is already repository-controlled and build-time compilation has a smaller runtime and security surface.

### Frontmatter-Only Content Access

Rejected because route generation and search need a common representation that also includes body-derived plain text.