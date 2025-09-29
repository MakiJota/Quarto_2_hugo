-- DEBUG: signal that the filter is loaded
print("✅ figure-wrapper.lua loaded")

-- Helper function to clean Quarto-specific attributes
function clean_figure(fig)
  print("Wrapping a figure...")

  -- Remove attributes on the Figure itself
  fig.attr.attributes["data-fig.cap"] = nil
  fig.attr.attributes["data-fig-align"] = nil
  fig.attr.attributes["data-fig-width"] = nil
  fig.attr.attributes["data-fig-height"] = nil
  fig.attr.attributes["data-fig-alt"] = nil
  fig.attr.attributes["data-fig-show"] = nil

  -- Traverse children to remove Quarto-specific attributes
  for i, child in ipairs(fig.content) do
    if child.t == "Para" then
      for _, inline in ipairs(child.content) do
        if inline.attr then
          inline.attr.attributes["aria-hidden"] = nil
        end
      end
    elseif child.t == "Image" then
      child.attr.attributes["data-fig.cap"] = nil
      child.attr.attributes["data-fig-align"] = nil
    end
  end

  -- Wrap in a div with debug message
  print("Figure wrapped in <div class='blog-content'>")
  return pandoc.Div({fig}, {class="blog-content"})
end

-- Handle standalone images (not already a Figure)
function Para(el)
  if #el.content == 1 and el.content[1].t == "Image" then
    local img = el.content[1]
    print("Found a standalone image: " .. img.src)
    local caption = pandoc.Inlines({pandoc.Str(img.alt)})
    local fig = pandoc.Figure({img}, caption, pandoc.Attr("", {}, {}))
    return clean_figure(fig)
  end
end

-- Handle Quarto-generated Figures (from R plots or Markdown fig.cap)
function Div(el)
  for i, v in ipairs(el.content) do
    if v.t == "Figure" then
      local caption_text = pandoc.utils.stringify(v.caption)
      print("Found a Quarto Figure with caption: " .. caption_text)
      return clean_figure(v)
    end
  end
end
