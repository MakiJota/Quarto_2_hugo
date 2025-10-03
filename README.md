# Quarto → Hugo Blog Pipeline

This project provides a **Quarto workflow** with a custom **Python post-processing script** to generate blog posts compatible with a **Hugo website**.  

It automates the conversion of `.qmd` → `.md`, wraps images and tables for Hugo, and enforces a clean folder structure for blog publishing.

---

## Project Structure

A typical setup looks like this:

```
│   _quarto.yml
│
├───01_input/              # input data files (RDS, CSV, etc.)
│       data_penguin.rds
│
├───asset/                 # images or other resources
│       image.png
│
├───content/               # Hugo blog output folder
│
├───filters/               # optional filters
│       figure-wrapper.lua
│
└───scripts/
    │   hugo_test.qmd       # your Quarto source
    │   postprocess_md.py   # Python postprocessor
```

---

## Quarto Configuration

The `_quarto.yml` should include the Hugo output and post-processing hook:

```yaml
project:
  type: hugo
  output-dir: content
  post-render:
    - python scripts/postprocess_md.py

format:
  hugo-md:
    code-fold: true
    #filters:
    #  - filters/figure-wrapper.lua

execute:
  warning: false
```

- **`postprocess_md.py`** wraps images and tables with Hugo-friendly markup.  
- Output is placed in `content/`.  

---

## Writing Posts

1. Create a new `.qmd` in `scripts/` (e.g., `hugo_test.qmd`).  
2. Add front matter metadata:  

```yaml
---
meta_title: "link from MD quarto FRESH FRESHY"
title: "link from MD quarto FRESH FRESHY"
description: "A quick analysis of the penguin dataset"
date: 2024-09-16
image: "/asset/culmen_depth.png"
categories: ["Data Science"]
author: "John Doe"
tags: ["R", "penguins"]
draft: false

format: 
  hugo-md: 
    variant: gfm 
    output-ext: md 
    keep-yaml: true
---
```

3. Include images directly — the postprocessor takes care of Hugo-compatible wrapping.  

---

## Special Markers for Tables

The postprocessor detects table layout markers to style them correctly.

### One Column Table
```markdown
<!-- table1:start -->
::: {style="display: flex; gap: 50px; flex-wrap: wrap; justify-content: center; text-align: center; width: 100px; padding: 100px;"}
::: {.columns}
### Average Bill Dimensions by Species
```{r}
data %>%
  group_by(species) %>% 
  summarise(average_bill_length = mean(bill_length_mm, na.rm = TRUE))
```
:::
:::
<!-- table1:end -->
```

### Two Column Table
```markdown
<!-- table2:start -->
::: {.columns}

::: {.column width="50%"}
### Average Bill Dimensions by Species
```{r}
data %>%
  group_by(species) %>% 
  summarise(average_bill_length = mean(bill_length_mm, na.rm = TRUE))
```
:::

::: {.column width="50%"}
### Average Bill Depth by Species
```{r}
data %>%
  group_by(species) %>% 
  summarise(average_bill_depth = mean(bill_depth_mm, na.rm = TRUE))
```
:::

:::
<!-- table2:end -->
```

✅ Use `<!-- table1:start --> ... <!-- table1:end -->` or  
`<!-- table2:start --> ... <!-- table2:end -->` to guide the script.  

---

## Workflow

1. Write your blog post in Quarto (`.qmd`) using R or Python.  
2. Render with:

   ```bash
   quarto render scripts/hugo_test.qmd
   ```

3. The generated `.md` will appear in `content/scripts/`.  
   - Rename it to **`index.md`**.  
   - Move it into the appropriate dated folder under `content/blog/`.  

   Example:
   ```
   content/blog/2024-09-16-my-post/index.md
   ```

4. Add any assets (images, etc.) in `asset/` and reference them in your `.qmd`.

---

## Notes

- `01_input/` (or any input folder) stores datasets for reproducibility.  
- `asset/` contains images or static resources.  
- Bibliography files (`.bib`) are supported by Quarto.  
- The **Python postprocessor** (`scripts/postprocess_md.py`) ensures that images and tables render properly in Hugo.  

---

## Quick Start

```bash
# Render a test post
quarto render scripts/hugo_test.qmd

# Move output into blog folder
mv content/scripts/hugo_test.md content/blog/2024-09-16-my-post/index.md
```

You now have a Hugo-ready blog post! 🚀
