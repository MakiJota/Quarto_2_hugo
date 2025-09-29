---
meta_title: link from MD quarto FRESH FRESHY
title: link from MD quarto FRESH FRESHY
description: A quick analysis of the penguin dataset
date: 2024-09-16T00:00:00.000Z
image: /asset/culmen_depth.png
categories:
  - Data Science
author: John Doe
tags:
  - R
  - penguins
draft: false
format:
  hugo-md:
    variant: gfm
    output-ext: md
    keep-yaml: true
---


## Introduction

This document offers a straightforward analysis of the well-known penguin dataset. It is designed to complement the [Productive R Workflow](https://www.productive-r-workflow.com) online course.

You can read more about the penguin dataset [here](https://allisonhorst.github.io/palmerpenguins/).

Let's load libraries before we start!

<details class="code-fold">
<summary>Code</summary>

``` r
# load the tidyverse
pacman::p_load(tidyverse,
  patchwork,
  knitr)     # combine charts together
```

</details>

## Loading data

The dataset has already been loaded and cleaned in the previous step of this pipeline.

Let's load the clean version, together with a few functions available in `functions.R`.

<details class="code-fold">
<summary>Code</summary>

``` r
# Source functions

# Read the clean dataset
data <- readRDS(file = "../01_input/data_pengvin.rds")
```

</details>

<div class="blog-content">
<figure>
<img src="asset/culmen_depth.png"  width="300" alt="Bill measurement explanation" />
<figcaption >Bill measurement explanation</figcaption>
</figure>
</div>

## Bill Length and Bill Depth

Now, let's make some descriptive analysis, including <b>summary statistics</b> and <b>graphs</b>.

What's striking is the <b>slightly negative relationship</b> between `bill length` and `bill depth`:

<details class="code-fold">
<summary>Code</summary>

``` r
# {r, fig.align = "center", fig.width=5, fig.height=5, warning=FALSE, fig.cap="Relationship between bill <b>length</b> and bill <b>depth</b>. <b>All</b> data points included."}

data %>%
  ggplot(aes(x = bill_length_mm, y = bill_depth_mm)) +
    geom_point(color = "#69b3a2") +
    labs(
      x = "Bill Length (mm)",
      y = "Bill Depth (mm)",
      title = "Surprising relationship?"
    ) +
    theme(
      legend.position = "none",
      panel.background = element_rect(fill = 'transparent', color = NA),
      plot.background  = element_rect(fill = 'transparent', color = NA),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      axis.line = element_line(color = "black", size = 0.5), # draws x and y axis lines only
      legend.background = element_rect(fill='transparent'),
      legend.box.background = element_rect(fill='transparent')
    )
```

</details>

<div class="blog-content">
<figure>
<img src="hugo_test.markdown_strict_files/figure-markdown_strict/unnamed-chunk-2-1.png" data-fig-align="center" width="480" alt="Relationship between bill length and bill depth. All data points included." />
<figcaption >Relationship between bill <b>length</b> and bill <b>depth</b>.<br><b>All</b> data points included.</figcaption>
</figure>
</div>

It is also interesting to note that `bill length` a and `bill depth` are quite different from one specie to another. This is summarized in the 2 tables below:

## one columna


<div id="table1" style="display: flex; gap: 50px; flex-wrap: wrap; justify-content: center; text-align: center;">
  <div>
### Average Bill Dimensions by Species

    # A tibble: 3 × 2
      species   average_bill_length
      <chr>                   <dbl>
    1 Adelie                   38.8
    2 Chinstrap                48.8
    3 Gentoo                   47.5
  </div>
</div>


## Two columnas


<div id="table2" style="display: flex; gap: 50px; flex-wrap: wrap; justify-content: center; text-align: center;">

  <div>
    <h5>Average Bill Dimensions by Species</h5>

    # A tibble: 3 × 2
      species   average_bill_length
      <chr>                   <dbl>
    1 Adelie                   38.8
    2 Chinstrap                48.8
    3 Gentoo                   47.5
  </div>

  <div>
    <h5>Average bill depth by species</h5>

    # A tibble: 3 × 2
      species   average_bill_depth
      <chr>                  <dbl>
    1 Adelie                  18.3
    2 Chinstrap               18.4
    3 Gentoo                  15.0
  </div>

</div>


Now, let's check the relationship between bill depth and bill length for the specie `Adelie` on the island `Torgersen`:

<details class="code-fold">
<summary>Code</summary>

``` r
create_scatterplot <- function(data, selected_species, color) {
  # Filter the data for the specified species and island
  filtered_data <- data %>%
    na.omit() %>%
    filter(species == selected_species)
  
  # Create the scatterplot
  plot <- ggplot(
    filtered_data,
    aes(x = bill_length_mm, y = bill_depth_mm)
  ) +
    geom_point(color=color) +
    labs(
      x = "Bill Length (mm)",
      y = "Bill Depth (mm)",
      title = selected_species
    )  +
    theme(
      legend.position = "none",
      panel.background = element_rect(fill = 'transparent', color = NA),
      plot.background  = element_rect(fill = 'transparent', color = NA),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      axis.line = element_line(color = "black", size = 0.5), # draws x and y axis lines only
      legend.background = element_rect(fill='transparent'),
      legend.box.background = element_rect(fill='transparent')
    )
  
  return(plot)

}

# Use the function in functions.R
p1 <- create_scatterplot(data, "Adelie", "#6689c6")
p2 <- create_scatterplot(data, "Chinstrap", "#e85252")
p3 <- create_scatterplot(data, "Gentoo", "#9a6fb0")

test <- p1 + p2 + p3 

test  & theme(plot.background = element_rect(fill='transparent', color=NA))
```

</details>

<div class="blog-content">
<figure>
<img src="hugo_test.markdown_strict_files/figure-markdown_strict/unnamed-chunk-6-1.png" width="864" alt="There is actually a positive correlation when split by species." />
<figcaption >There is actually a positive correlation when split by species.</figcaption>
</figure>
</div>
