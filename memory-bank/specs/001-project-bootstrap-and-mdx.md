# Project Bootstrap and MDX

## Purpose

Establish the initial Spec Driven Development Demo application and the authoring path for educational articles. The application must be a Next.js 16 site styled with Tailwind CSS 4. It must render version-controlled MDX articles and make their metadata and searchable text available to application features.

## Goals

- Create a TypeScript-based Next.js 16 application using the App Router.
- Configure Tailwind CSS 4 for application and MDX typography.
- Store articles as MDX files in the repository.
- Render article routes from MDX content and frontmatter.
- Expose a normalized article collection for navigation and future Fuse.js search.
- Provide a small, documented set of React components that MDX authors may use.

## Non-Goals

- A CMS, database, authoring UI, or remote content source.
- Runtime compilation of untrusted MDX.
- Full-text search interface and ranking behavior. This spec prepares the content data needed for a later search spec.
- Authentication, analytics, localization, comments, or content versioning beyond Git.

## Bootstrap Requirements

### Application

- Use Next.js 16, React, TypeScript, and the App Router.
- Keep the default application source under `src/`.
- Define the site root, a global layout, global styles, and a home page.
- The home page must list published articles with their title, description, tags, and publication date.
- Provide an article route at `/articles/[slug]`.
- Use static generation for the article index and each article route.
- Include package scripts for local development, production build, production start, linting, and type checking.

### Styling

- Configure Tailwind CSS 4 using its supported Next.js integration.
- Apply prose styles to rendered MDX content using the Tailwind Typography plugin or an equivalent local style layer.
- Keep application-wide style tokens and base styles in the global stylesheet.
- Do not couple article prose styling to any individual MDX file.

## Content Model

### Content Location

- Store source articles under `content/articles/`.
- Treat each `*.mdx` file in that directory as one article.
- Derive an article's `slug` from its filename. For example, `content/articles/agent-skills.mdx` produces `/articles/agent-skills`.
- Do not permit nested article paths in the first implementation.

### Required Frontmatter

Every article must begin with YAML frontmatter containing:

```yaml
title: String
description: String
publishedAt: YYYY-MM-DD
tags:
  - string
published: true
```

- `title` must be non-empty.
- `description` must be non-empty and suitable for a list preview.
- `publishedAt` must be a valid calendar date.
- `tags` must be an array of non-empty strings.
- `published` must be a boolean.
- `slug` must not be supplied in frontmatter.

Additional frontmatter fields must be rejected until a later spec explicitly introduces them.

### Normalized Article Shape

The content module must expose a normalized article record with:

```ts
type Article = {
  slug: string;
  title: string;
  description: string;
  publishedAt: string;
  tags: string[];
  published: boolean;
  content: string;
  searchText: string;
};
```

- `content` is the MDX body with its frontmatter removed.
- `searchText` is plain text derived from the title, description, tags, and MDX body; it must not include frontmatter syntax or rendered markup.
- Published collections and routes must exclude articles where `published` is `false`.
- Sort published article listings by `publishedAt` descending, then `title` ascending.

## MDX Integration

- Configure `@next/mdx` with `@mdx-js/loader` and `@mdx-js/react` for `.md` and `.mdx` support.
- Render repository content as trusted build-time code only.
- Parse and validate frontmatter before an article appears in a list, route, or static-param generation.
- Fail the build with the source file path and validation issue when frontmatter is invalid or a slug is duplicated.
- Use a shared MDX component map for article rendering.
- The initial supported MDX component map must include semantic overrides for headings, links, paragraphs, lists, code blocks, and a `Callout` component.
- MDX files must not import arbitrary application modules. Add new author-facing components through the shared component map and document them near that map.

## Routing and Rendering

- Generate article route params from published article slugs.
- Render a not-found response for unknown or unpublished article slugs.
- Each article page must include its title, description, publication date, tags, and MDX body.
- Supply article metadata from frontmatter for the page title and description.
- Use the article slug as the stable identifier for React lists and search results.

## Initial Content

- Add one published example article that uses headings, a link, a fenced code block, a list, and `Callout`.
- The example must exercise frontmatter parsing and the MDX component map.

## Acceptance Criteria

- `npm run dev` starts the application without MDX configuration errors.
- `npm run build` statically generates the home page and the example article page.
- The home page lists the example article and links to `/articles/<example-slug>`.
- The article route renders its frontmatter and MDX body with prose styling.
- An unpublished article is absent from the home page and returns not found at its article route.
- An invalid frontmatter field, invalid frontmatter type, or duplicate filename-derived slug fails the build with an actionable error.
- The content module returns `searchText` suitable for a future Fuse.js index.

## Follow-Up Work

- Define the search interaction, Fuse.js index lifecycle, filters, and empty states.
- Define an article table of contents and heading-anchor behavior.
- Establish accessibility requirements for custom MDX components.