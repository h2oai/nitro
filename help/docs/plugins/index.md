---
template: overrides/main.html
---

# Plugins

Plugins add new capabilities to Nitro. See [writing plugins](writing.md) to learn how to write your own plugins.

!!! warning
    Plugins use Javascript, and are only supported for web apps.
    Avoid using plugins if you're targeting mobile or desktop apps.

## Data Visualization

### Bokeh

Renders [Bokeh](https://docs.bokeh.org/en/latest/) visualizations.

!!!example "Install"
    ```sh
    pip install h2o-nitro-bokeh
    ```

[:material-github: Github](https://github.com/h2oai/nitro-bokeh)

### Matplotlib / Seaborn

Renders [Matplotlib](https://matplotlib.org/stable/index.html) and [Seaborn](https://seaborn.pydata.org/)
visualizations.

!!!example "Install"
    ```sh
    pip install h2o-nitro-matplotlib
    ```

[:material-github: Github](https://github.com/h2oai/nitro-matplotlib)

### Altair

Renders [Altair](https://altair-viz.github.io/), [Vega](https://vega.github.io/vega/)
, [Vega-Lite](https://vega.github.io/vega-lite/) visualizations.

!!!example "Install"
    ```sh
    pip install h2o-nitro-altair
    ```

[:material-github: Github](https://github.com/h2oai/nitro-altair)

## List your plugins here!

Don't forget to let us know about your plugins and make them available to the community.

We'll be happy to include your plugin on this page - simply drop us a note, or submit a PR
for this page, or [file an issue](https://github.com/h2oai/nitro/issues/new/choose) in our Github repo.
