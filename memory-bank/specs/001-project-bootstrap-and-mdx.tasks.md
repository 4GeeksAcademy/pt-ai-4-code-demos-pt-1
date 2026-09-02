# Tasks: Project Bootstrap and MDX

Source: [001-project-bootstrap-and-mdx.md](./001-project-bootstrap-and-mdx.md)

## 1. Initialize the Next.js Application

- [ ] Scaffold a Next.js 16 application with TypeScript and the App Router under `src/`.
- [ ] Add scripts for `dev`, `build`, `start`, `lint`, and type checking.
- [ ] Add the root layout, global stylesheet, and minimal home route.
- [ ] Verify `npm run dev` starts without application configuration errors.

## 2. Configure Tailwind and Typography

- [ ] Configure Tailwind CSS 4 using its supported Next.js integration.
- [ ] Add the Tailwind Typography plugin or an equivalent reusable prose style layer.
- [ ] Define global style tokens and base styles in the global stylesheet.
- [ ] Verify prose styles apply through a shared class or component rather than article-local CSS.

## 3. Configure Build-Time MDX

- [ ] Install and configure `@next/mdx`, `@mdx-js/loader`, and `@mdx-js/react` for `.md` and `.mdx` files.
- [ ] Add the MDX provider integration required by the App Router.
- [ ] Create the shared MDX component map with overrides for headings, links, paragraphs, lists, and fenced code blocks.
- [ ] Implement and register the `Callout` component.
- [ ] Document the supported MDX component map beside its implementation.
- [ ] Verify a minimal MDX fixture compiles during `npm run build`.

## 4. Build the Article Content Module

- [ ] Add `content/articles/` as the only initial article source directory.
- [ ] Define the `Article` TypeScript shape from the specification.
- [ ] Read top-level `*.mdx` files and derive slugs from filenames.
- [ ] Parse YAML frontmatter and separate it from the MDX body.
- [ ] Validate frontmatter with a strict schema: required keys only, non-empty title and description, valid date, non-empty tag strings, and boolean `published`.
- [ ] Reject author-provided `slug` values, nested article paths, invalid fields/types, and duplicate derived slugs with errors that name the source file.
- [ ] Generate plain `searchText` from title, description, tags, and the body, excluding frontmatter and markup.
- [ ] Expose helpers to retrieve published listings and individual published articles, sorted by date descending then title ascending.
- [ ] Add focused tests for normalization, sorting, `searchText`, validation failures, duplicate slugs, and unpublished filtering.

## 5. Add Example Content Fixtures

- [ ] Create one published article with all required frontmatter.
- [ ] Include headings, a link, a fenced code block, a list, and `Callout` in the published article.
- [ ] Create one unpublished article fixture for route and listing coverage.
- [ ] Verify article fixtures are valid through the content module tests.

## 6. Implement Article Listing and Routes

- [ ] Render published articles on the home page with title, description, tags, publication date, and a link keyed by slug.
- [ ] Add `/articles/[slug]` with static params generated from published article slugs.
- [ ] Render article title, description, publication date, tags, and MDX body with the shared prose style layer.
- [ ] Return Next.js not-found for unknown or unpublished slugs.
- [ ] Produce route metadata from the article title and description.
- [ ] Add route-level tests or equivalent integration coverage for listing, metadata, article rendering, and not-found behavior.

## 7. Validate the Delivery

- [ ] Run type checking.
- [ ] Run linting.
- [ ] Run focused content and route tests.
- [ ] Run `npm run build` and confirm static generation includes the home page and published article.
- [ ] Manually verify the home page link, rendered article content, and unpublished article not-found response in a production build.

## Completion Criteria

All tasks are complete when every acceptance criterion in the source specification passes, the production build succeeds, and the content module's tests cover both valid articles and the specified invalid-content failures.