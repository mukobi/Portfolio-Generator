# Portfolio-Generator

Generates my portfolio sites using Python, YAML, and Jinja2 and statically serves them over GitHub pages.

## About 

I got really tired of having to manually update the HTML of my statically-hosted software portfolio, so I decided to be a real programmer and write a tool to automate it. Gone are the days of copy-pasting the previous project's div, searching around for all the right spots to change the titles and descriptions, and then getting frustrated when I want to reorder things or change a similar detail across multiple pages.

Instead, for any of my portfolio sites (including the one you're looking at now), this Python script reads meta files stored as YAML for each page or project, evaluates them against a set of templates using Jinja2, and copies over all other source files like images, JS, or CSS. The compiled HTML and copied files are neatly placed together, responsive CSS makes everything dynamically fit together well, and I can freely and efficiently share my work on a static site host and CDN.

[See here for my portfolio sites](https://gabrielmukobi.com/#portfolio) built using this tool.

## Special Compilation Notes

### Photos

- If adding new photos, you may need to run the 2 scripts in the `precompile` folder first. These add metadata and generate thumbnails for the dense gallery functionality. They should be run automatically by the compilation script, but you can also run them manually if it's not working.
