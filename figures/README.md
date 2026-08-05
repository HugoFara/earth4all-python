# Figures

Drawn by `python scripts/render_figures.py`, from the model in this repository.

Units are the ones the model carries: `Mp` is millions of people, `G$` a billion
dollars, `Mha` a million hectares, `Gcu` a billion capacity units, and `(1)` a
quantity that has no unit at all — a share, a ratio, or an index.

## The two scenarios

| Too Little Too Late | Giant Leap |
| --- | --- |
| ![Too Little Too Late base run](baserun-tltl.png) | ![Giant Leap base run](baserun-gl.png) |

The same six variables with the scenarios drawn on top of each other:

![The two scenarios compared](scenario-comparison.png)

## The twelve sectors

Each sector is run on its own here, with the variables the other eleven would
have given it read from tabulated runs of the whole model, which is what
`<sector>.<name>_run()` composes. Every figure is the one its `fig_*` function
draws, with the vertical axes shown.

### Climate

Warming, the gases behind it, and the ice left.

![Climate sector](sectors/climate.png)

### Demand

How output is split between consumption, savings and the state, and how much debt households and governments carry.

![Demand sector](sectors/demand.png)

### Energy

The cost of the energy the world uses.

![Energy sector](sectors/energy.png)

### Finance

The signal rate the central bank sets and the borrowing costs that follow it, over the two decades around 2020.

![Finance sector](sectors/finance.png)

### Food and land

Cropland, what is grown on it, the fertiliser it takes, and the land left to regenerate.

![Food and land sector](sectors/foodland.png)

### Inventory

Stocks against desired stocks, and the inflation that comes of the gap.

![Inventory sector](sectors/inventory.png)

### Labour market

The size of the workforce, its share of output, and unemployment.

![Labour market sector](sectors/labourmarket.png)

### Other

The cost of the turnarounds, the people below the poverty line, and the growth of output per person.

![Other sector](sectors/other.png)

### Output

The capital stock in private and public hands, and the output it yields.

![Output sector](sectors/output.png)

### Population

Births, life expectancy past sixty, and the population that results.

![Population sector](sectors/population.png)

### Public

Public spending, the tax that funds it, and the productivity it buys.

![Public sector](sectors/public.png)

### Wellbeing

The average wellbeing index, which the whole model is built to explain.

![Wellbeing sector](sectors/wellbeing.png)
