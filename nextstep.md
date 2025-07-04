# Next Steps: Building the Documentation Website

This document outlines the plan to create a modern, professional documentation website for the RabbitHole project using Astro and Svelte, with automated deployment to GitHub Pages.

---

### **Phase 1: Project Setup & Configuration**

1.  **Scaffold Astro Project:**
    -   Create a new Astro project in a `website/` directory at the project root.
    -   This will be a minimal setup designed for content-focused sites.

2.  **Add Svelte Integration:**
    -   Integrate Svelte into the Astro project to allow for the use of interactive components if needed in the future.

3.  **Configure for GitHub Pages:**
    -   Modify the `astro.config.mjs` file to set the correct `site` and `base` URLs. This is essential for ensuring that assets (CSS, JS, images) load correctly when deployed to a subdirectory on GitHub Pages (e.g., `https://username.github.io/RabbitHole/`).

---

### **Phase 2: Content Migration**

1.  **Copy Documentation Files:**
    -   Copy all existing Markdown files from the `docs/` directory into the new `website/src/content/docs/` directory. Astro uses a content collections system that will automatically turn these files into pages.

2.  **Establish a Main "Docs" Page:**
    -   Create a main `index.mdx` file within the `website/src/pages/docs/` directory that will serve as the landing page for the documentation section.

---

### **Phase 3: Automated Deployment**

1.  **Create GitHub Actions Workflow:**
    -   Add a new workflow file at `.github/workflows/deploy-docs.yml`.

2.  **Define Workflow Steps:**
    -   **Trigger:** The workflow will trigger automatically on every `push` to the `main` branch.
    -   **Setup:** It will check out the code, set up Node.js, and install the website's dependencies (`npm install`).
    -   **Build:** It will run the `npm run build` command to generate the static website files.
    -   **Deploy:** It will use a community action (`actions/deploy-pages`) to push the built files to the `gh-pages` branch, which automatically publishes them to GitHub Pages.

---

### **Final Outcome**

Upon completion of these steps, the RabbitHole project will have a fast, modern, and professional documentation website that updates automatically with every change to the `main` branch. The site will be accessible at `https://<your-github-username>.github.io/RabbitHole`. 