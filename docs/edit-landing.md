---
title: Edit Landing
area: home
edit_url: ""
---

# Edit Landing

Welcome! Before you start editing, please read the guidelines below.

## Editing Rules

### 1. Frontmatter Format

Every page **must** have this frontmatter at the top:

```yaml
---
title: Concept Name
area: foundations          # one of the 10 pillars
prerequisites:
  - prerequisite-concept   # concept IDs that must be understood first
related:
  - related-concept         # conceptually related pages
difficulty: 1               # 1 = basic, 2 = intermediate, 3 = advanced
status: draft
quality_score: 0            # auto-calculated, leave as 0
---
```

### 2. Writing Style

- **Definitions first**: Every concept page must start with a precise definition
- **Proved theorems**: Every theorem must have a proof (or mark as *unproved* with a reference)
- **Prerequisites explicit**: Use `prerequisites` frontmatter to guide readers
- **Link generously**: Use `[]()` markdown links to connect related concepts
- **LaTeX math**: Use `$...$` for inline math and `$$...$$` for display math

### 3. Page Structure

```markdown
# Title

## Definition

## Properties / Theorem

### Proof

## Examples

## Related Concepts
- [Related 1](related-1.md)
- [Related 2](related-2.md)
```

### 4. Do Not

- Do **not** add content without frontmatter (build will fail)
- Do **not** link to external pages without good reason (wiki is self-contained)
- Do **not** leave `difficulty` blank or set `quality_score` manually
- Do **not** commit `concepts.db` or `concepts.json` — they are auto-generated

## Start Editing

<div id="start-edit-container" style="text-align: center; margin: 2rem 0;">
  <a id="start-edit-link" href="#" class="md-button md-button--primary" style="font-size: 1.2rem; padding: 0.8rem 1.5rem;">
    :material-pencil: Start Editing on GitHub
  </a>
</div>

<script>
  // Get the ?ref= parameter from the URL
  const params = new URLSearchParams(window.location.search);
  const ref = params.get('ref') || '';
  
  // Build the GitHub edit URL
  const repoUrl = 'https://github.com/QQSHI13/lemma/edit/main/docs/';
  const editUrl = repoUrl + ref;
  
  // Update the link
  document.getElementById('start-edit-link').href = editUrl;
  
  // If no ref, show a message
  if (!ref) {
    document.getElementById('start-edit-container').innerHTML = 
      '<p style="color: var(--md-default-fg-color--light);">No page specified. Navigate to a page and click the "Edit" icon.</p>';
  }
</script>

## License

By contributing, you agree that your content will be licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

---

Built with [DocsForge](https://github.com/QQSHI13/docsforge).
