# import libs
import pandas as pd
import numpy as np
from plotnine import *

# some constants
c_remote_data ='https://raw.githubusercontent.com/nickhould/craft-beers-dataset/master/data/processed/beers.csv'
c_col = ["#2f4858", "#f6ae2d", "#f26419",
         "#33658a", "#55dde0", "#2f4858",
         "#2f4858", "#f6ae2d", "#f26419",
         "#33658a", "#55dde0", "#2f4858"]

# useful functions
def labels(from_, to_, step_):
    return pd.Series(np.arange(from_, to_ + step_, step_)).apply(lambda x: '{:,}'.format(x)).tolist()

def breaks(from_, to_, step_):
    return pd.Series(np.arange(from_, to_ + step_, step_)).tolist()

# read data
data = pd.read_csv(c_remote_data)

data = (
    data.filter([
        'abv',
        'ibu',
        'id',
        'name',
        'style',
        'brewery_id',
        'ounces'
    ]).
    set_index('id')
)

# some descriptions

data.head()

data.abv.describe()

# histogram
fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_histogram(aes(x = 'abv'))
)

fig

fig.save('./02-output/01.jpg')

# adding color
fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_histogram(
        aes(x = 'abv'),
        fill = c_col[0], color = 'black'
    )
)

fig

fig.save('./02-output/02.jpg')

# adding labels
fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_histogram(
        aes(x = 'abv'),
        fill = c_col[0], color = 'black'
    ) +
    labs(
        title ='Distribution of The alcoholic content by volume (abv)',
        x = 'abv - The alcoholic content by volume',
        y = 'Count',
    )
)

fig

fig.save('./02-output/03.jpg')


# manipulating axes
fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_histogram(
        aes(x = 'abv'),
        fill = c_col[0], color = 'black'
    ) +
    labs(
        title ='Distribution of The alcoholic content by volume (abv)',
        x = 'abv - The alcoholic content by volume',
        y = 'Count',
    ) +
    scale_x_continuous(
        limits = (0, 0.14),
        labels = labels(0, 0.14, 0.02),
        breaks = breaks(0, 0.14, 0.02)
    ) +
    scale_y_continuous(
        limits = (0, 350),
        labels = labels(0, 350, 50),
        breaks = breaks(0, 350, 50)
    )
)

fig

fig.save('./02-output/04.jpg')

# apply a theme
theme_set(
    theme_538()
)

fig.save('./02-output/05.jpg')

# change theme features
theme_set(
    theme_538() +
    #theme_xkcd()+
    theme(
        figure_size = (8, 4),
        text = element_text(
            size = 8,
            color = 'black',
            family = 'Arial'
        ),
        plot_title = element_text(
            color = 'black',
            family = 'Arial',
            weight = 'bold',
            size = 12
        ),
        axis_title = element_text(
            color = 'black',
            family = 'Arial',
            weight = 'bold',
            size = 6
        ),
    )
)
fig.save('./02-output/06.jpg')

# add some statistics

fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_histogram(
        aes(x = 'abv'),
        fill = c_col[0], color = 'black'
    ) +
    labs(
        title ='Distribution of The alcoholic content by volume (abv)',
        x = 'abv - The alcoholic content by volume (median = dashed line; mean = solid line)',
        y = 'Count',
    ) +
    scale_x_continuous(
        limits = (0, 0.14),
        labels = labels(0, 0.14, 0.02),
        breaks = breaks(0, 0.14, 0.02)
    ) +
    scale_y_continuous(
        limits = (0, 350),
        labels = labels(0, 350, 50),
        breaks = breaks(0, 350, 50)
    ) +
    geom_vline(aes(xintercept = data.abv.mean()), color = 'gray') +
    geom_vline(aes(xintercept = data.abv.median()), linetype = 'dashed', color = 'gray')
)

fig

fig.save('./02-output/07.jpg')

# faceting

fig = (
    ggplot(data.dropna(subset = ['abv', 'style'])[data['style'].dropna().str.contains('American')]) +
    geom_histogram(
        aes(x = 'abv'),
        fill = c_col[0], color = 'black'
    ) +
    labs(
        title ='Distribution of The alcoholic content by volume (abv)',
        x = 'abv - The alcoholic content by volume',
        y = 'Count',
    ) +
    scale_x_continuous(
        limits = (0, 0.14),
        labels = labels(0, 0.14, 0.07),
        breaks = breaks(0, 0.14, 0.07)
    ) +
    scale_y_continuous(
        limits = (0, 300),
        labels = labels(0, 300, 100),
        breaks = breaks(0, 300, 100)
    ) +
    theme(figure_size = (8, 12)) +
    facet_wrap('~style', ncol = 4)
)

fig

fig.save('./02-output/08.jpg')

# Scatterplot

fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_point(
        aes(x = 'abv',
            y = 'ibu'),
        fill = c_col[0], color = 'black'
    ) +
    labs(
        title ='Relationship between alcoholic content (abv) and int. bittering untis (ibu)',
        x = 'abv - The alcoholic content by volume',
        y = 'ibu - International bittering units',
    ) +
    scale_x_continuous(
        limits = (0, 0.14),
        labels = labels(0, 0.14, 0.02),
        breaks = breaks(0, 0.14, 0.02)
    )  +
    scale_y_continuous(
        limits = (0, 150),
        labels = labels(0, 150, 30),
        breaks = breaks(0, 150, 30)
    )
)

fig

fig.save('./02-output/09.jpg')



fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_point(
        aes(x = 'abv',
            y = 'ibu',
            size = 'ounces'),
        fill = c_col[0], color = 'black'
    ) +
    labs(
        title ='Relationship between alcoholic content (abv) and int. bittering untis (ibu)',
        x = 'abv - The alcoholic content by volume',
        y = 'ibu - International bittering units',
    ) +
    scale_x_continuous(
        limits = (0, 0.14),
        labels = labels(0, 0.14, 0.02),
        breaks = breaks(0, 0.14, 0.02)
    )  +
    scale_y_continuous(
        limits = (0, 150),
        labels = labels(0, 150, 30),
        breaks = breaks(0, 150, 30)
    )
)

fig

fig.save('./02-output/10.jpg')


data['ounces_str'] = data['ounces']
data['ounces_str'] = data['ounces_str'].apply(str)

fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_point(
        aes(x = 'abv',
            y = 'ibu',
            fill = 'ounces_str'),
        alpha = 0.5,
        color = 'black'
    ) +
    labs(
        title ='Relationship between alcoholic content (abv) and int. bittering untis (ibu)',
        x = 'abv - The alcoholic content by volume',
        y = 'ibu - International bittering units',
    ) +
    scale_fill_manual(
        name = 'Ounces',
        values = c_col) +
    scale_x_continuous(
        limits = (0, 0.14),
        labels = labels(0, 0.14, 0.02),
        breaks = breaks(0, 0.14, 0.02)
    )  +
    scale_y_continuous(
        limits = (0, 150),
        labels = labels(0, 150, 30),
        breaks = breaks(0, 150, 30)
    )
)

fig

fig.save('./02-output/11.jpg')


fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_point(
        aes(x = 'abv',
            y = 'ibu',
            fill = 'ounces_str'),
        alpha = 0.5,
        color = 'black'
    ) +
    geom_smooth(
        aes(x = 'abv',
            y = 'ibu')
    ) +
    labs(
        title ='Relationship between alcoholic content (abv) and int. bittering untis (ibu)',
        x = 'abv - The alcoholic content by volume',
        y = 'ibu - International bittering units',
    ) +
    scale_fill_manual(
        name = 'Ounces',
        values = c_col) +
    scale_x_continuous(
        limits = (0, 0.14),
        labels = labels(0, 0.14, 0.02),
        breaks = breaks(0, 0.14, 0.02)
    )  +
    scale_y_continuous(
        limits = (0, 150),
        labels = labels(0, 150, 30),
        breaks = breaks(0, 150, 30)
    )
)

fig

fig.save('./02-output/12.jpg')


fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_jitter(
        aes(x = 'abv',
            y = 'ibu',
            fill = 'ounces_str'),
        width = 0.0051,
        height = 5,
        color = 'black'
    ) +
    labs(
        title ='Relationship between alcoholic content (abv) and int. bittering untis (ibu)',
        x = 'abv - The alcoholic content by volume',
        y = 'ibu - International bittering units',
    ) +
    scale_fill_manual(
        guide = False,
        name = 'Ounces',
        values = c_col) +
    scale_x_continuous(
        limits = (0, 0.14),
        labels = labels(0, 0.14, 0.02),
        breaks = breaks(0, 0.14, 0.02)
    )  +
    scale_y_continuous(
        limits = (0, 150),
        labels = labels(0, 150, 30),
        breaks = breaks(0, 150, 30)
    ) +
    facet_wrap('ounces_str')
)

fig

fig.save('./02-output/13.jpg')


fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_bin2d(
        aes(x = 'abv',
            y = 'ibu')
    ) +
    labs(
        title ='Relationship between alcoholic content (abv) and int. bittering untis (ibu)',
        x = 'abv - The alcoholic content by volume',
        y = 'ibu - International bittering units',
    ) +
    scale_x_continuous(
        limits = (0, 0.14),
        labels = labels(0, 0.14, 0.02),
        breaks = breaks(0, 0.14, 0.02)
    )  +
    scale_y_continuous(
        limits = (0, 150),
        labels = labels(0, 150, 30),
        breaks = breaks(0, 150, 30)
    ) +
    theme(figure_size = (8, 8))
)

fig

fig.save('./02-output/14.jpg')


fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_boxplot(
        aes(x = 'ounces_str',
            y = 'abv')
    ) +
    labs(
        title ='Distribution of alcoholic content (abv) by size',
        x = 'size in ounces',
        y = 'abv - The alcoholic content by volume',
    ) +
    scale_y_continuous(
        limits = (0, 0.14),
        labels = labels(0, 0.14, 0.02),
        breaks = breaks(0, 0.14, 0.02)
    )
)

fig

fig.save('./02-output/15.jpg')


fig = (
    ggplot(data.dropna(subset = ['abv'])) +
    geom_violin(
        aes(x = 'ounces_str',
            y = 'abv'),
        fill = c_col[0]
    ) +
    labs(
        title ='Distribution of alcoholic content (abv) by size',
        x = 'size in ounces',
        y = 'abv - The alcoholic content by volume',
    ) +
    scale_y_continuous(
        limits = (0, 0.14),
        labels = labels(0, 0.14, 0.02),
        breaks = breaks(0, 0.14, 0.02)
    )
)

fig

fig.save('./02-output/16.jpg')
