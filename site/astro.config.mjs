import { defineConfig } from 'astro/config';

// Update these values with your GitHub username and repo name.
// Site URL: https://<GITHUB_USERNAME>.github.io
// Base path: /<GITHUB_REPO>
//
// If using a custom domain, set site to your domain and base to '/'.

export default defineConfig({
  site: 'https://MohammedYaseen97.github.io',
  base: '/markov-thinks-slow',
  trailingSlash: 'ignore',
  build: {
    format: 'directory',
  },
});
