import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import sqlalchemy as sql

from matplotlib import pyplot as plt


def read_sql(engine, query):
    """
    :param engine: SQLite database engine.
    :param query: SQL query.
    :return: Pandas DataFrame.
    """
    return pd.read_sql_query(query, engine)


def plot_data(title, xlabel=None, ylabel=None):
    """
    :param title: Title of the plot.
    :param xlabel: Label of the x-axis.
    :param ylabel: Label of the y-axis.
    """
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(os.path.join('../data/plots/', title.replace(' ', '_') + '.png'))


def plot_radar(num_boroughs, ax, data, title, alpha, color):
    angles = [n / float(num_boroughs) * 2 * np.pi for n in range(num_boroughs)]
    data = data.values.tolist()
    angles += angles[:1]
    data += data[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.plot(angles, data, linewidth=2, linestyle='solid', label=title, color=color)
    ax.fill(angles, data, alpha=alpha, color=color)


def main():
    # Specify the SQLite database engine.
    engine = sql.create_engine('sqlite:///../data/data.sqlite')
    data_directory = '../data/plots/'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    # Fetching data for each analysis from the respective tables
    query_dict = {
        'life_satisfaction_query': "SELECT area_name, average_age, life_satisfaction_score "
                                   "FROM london_borough_profiles ORDER BY average_age, life_satisfaction_score",
        'bame_population_query': "SELECT area_name, pctg_population_bame "
                                 "FROM london_borough_profiles ORDER BY pctg_population_bame",
        'crime_query': "SELECT A.borough, A.major_category, SUM(A.value) AS total_count "
                       "FROM london_crime_by_lsoa as A "
                       "INNER JOIN london_borough_profiles as B ON A.borough = B.area_name "
                       "GROUP BY borough, major_category",
        'crime_amount_query': "SELECT A.borough, SUM(A.value) AS total_count FROM london_crime_by_lsoa as A "
                              "INNER JOIN london_borough_profiles as B ON A.borough = B.area_name "
                              "GROUP BY A.borough ORDER BY total_count",
        'house_price_query': "SELECT A.area, A.date, A.mean_house_price FROM housing_in_london_monthly as A "
                             "INNER JOIN london_borough_profiles as B ON A.area = LOWER(B.area_name)",
        'gross_annual_pay_query': "SELECT area_name, gross_annual_pay FROM london_borough_profiles "
                                  "ORDER BY gross_annual_pay",
        'health_query': "SELECT area_name, male_life_expectancy, female_life_expectancy, population_density, "
                        "prop_population_over_65 FROM london_borough_profiles",
        'education_query': "SELECT area_name, prop_working_age_no_qualif, prop_working_age_degree, "
                           "achvmt_5_or_more_gcse, gross_annual_pay, employment_rate "
                           "FROM london_borough_profiles ORDER BY prop_working_age_no_qualif",
        'transport_env_query': "SELECT area_name, number_of_cars, avg_public_transport_accessibility, "
                               "pctg_area_greenspace FROM london_borough_profiles ORDER BY number_of_cars",
        'political_analysis_query': "SELECT area_name, prop_seats_conservatives_2014_elect, "
                                    "prop_seats_labour_2014_elect, prop_seats_lib_dems_2014_elect "
                                    "FROM london_borough_profiles ORDER BY prop_seats_conservatives_2014_elect, "
                                    "prop_seats_labour_2014_elect, prop_seats_lib_dems_2014_elect",
        'political_turnout_query': "SELECT area_name, turnout_2014_local_elect FROM london_borough_profiles "
                                   "ORDER BY turnout_2014_local_elect DESC",
        'wellbeing_scores_query': "SELECT area_name, life_satisfaction_score, happiness_score, anxiety_score, "
                                  "worthwhileness_score FROM london_borough_profiles"
    }

    # Read the data from the SQLite database into Pandas DataFrames
    data_frames = {re.sub(r'_query$', '', key): read_sql(engine, query_dict[key]) for key in query_dict}

    # Plotting the data

    # Life Satisfaction and Demographic Analysis

    # Plotting the life satisfaction score vs average age
    sns.set_style('whitegrid')
    data_frames['life_satisfaction']['area_name'] = [area[:12] + '..' if len(area) > 12 else area for area in
                                                     data_frames['life_satisfaction']['area_name']]
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=data_frames['life_satisfaction'], x='average_age', y='life_satisfaction_score', s=100)
    for i, area in enumerate(data_frames['life_satisfaction']['area_name']):
        plt.text(data_frames['life_satisfaction']['average_age'][i] + 0.1,
                 data_frames['life_satisfaction']['life_satisfaction_score'][i] + 0.0025, area)
    plt.grid(True)
    plot_data('Life Satisfaction Score vs Average Age', 'Average Age', 'Life Satisfaction Score [#]')

    # Plotting the average age and life satisfaction vs area
    sns.set_style('whitegrid')
    sub_frame = data_frames['life_satisfaction']
    sub_frame.set_index('area_name', inplace=True)
    fig, ax1 = plt.subplots(figsize=(15, 12))
    color = 'tab:green'
    sub_frame['average_age'].plot(kind='bar', ax=ax1, width=.4, color=color, label='Average Age', position=1)
    plt.xticks(rotation=45)
    ax1.set_xlabel('Borough')
    ax1.set_ylabel('Average Age')
    ax1.set_ylim(30, 42.5)
    ax1.grid(True)
    ax2 = ax1.twinx()
    color = 'tab:blue'
    sub_frame['life_satisfaction_score'].plot(kind='bar', ax=ax2, width=.4, color=color,
                                              label='Life Satisfaction Score', position=0)
    plt.xticks(rotation=45)
    ax2.set_ylabel('Life Satisfaction Score')
    ax2.set_ylim(6.5, 7.75)
    ax2.grid(False)
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
    title = 'Average Age and Life Satisfaction Score per Borough'
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join('../data/plots/', title.replace(' ', '_') + '.png'))

    # Plotting the BAME population percentage
    sns.set_style('whitegrid')
    data_frames['bame_population']['area_name'] = [area[:12] + '..' if len(area) > 12 else area for area in
                                                   data_frames['bame_population']['area_name']]
    plt.figure(figsize=(14, 12))
    plt.xticks(rotation=45)
    sns.barplot(data=data_frames['bame_population'], x='area_name', y='pctg_population_bame')
    plot_data('Percentage of Population from BAME Groups per Borough', 'Borough',
              'Percentage of BAME groups [%]')

    # Crime Analysis

    # Plotting the crime rate per borough
    sns.set_style('whitegrid')
    data_frames['crime']['borough'] = [area[:12] + '..' if len(area) > 12 else area for area in
                                       data_frames['crime']['borough']]
    data_frames['crime_amount']['borough'] = [area[:12] + '..' if len(area) > 12 else area for area in
                                              data_frames['crime_amount']['borough']]
    sub_frame = data_frames['crime'].groupby(['borough', 'major_category'])['total_count'].sum().unstack()
    sub_frame = sub_frame.reindex(data_frames['crime_amount']['borough'].tolist())
    sub_frame.plot(kind='bar', stacked=True, figsize=(13, 13))
    plt.xticks(rotation=45)
    plt.legend(title='Major Crime Category', loc='upper left')
    plot_data('Crime Amount per Borough', 'Borough', 'Counted Crimes')

    # Housing and Economic Analysis

    # Plotting the house price per month for the ten most expensive and cheapest boroughs
    sns.set_style('whitegrid')
    data_frames['house_price']['area'] = [area[:12] + '..' if len(area) > 12 else area for area in
                                          data_frames['house_price']['area']]
    sub_frame = data_frames['house_price']
    cheapest_boroughs = sub_frame[sub_frame['date'] == '2014/01/01'].sort_values(
        by='mean_house_price', ascending=True).head(10)['area'].tolist()
    expensive_boroughs = sub_frame[sub_frame['date'] == '2014/01/01'].sort_values(
        by='mean_house_price', ascending=False).head(10)['area'].tolist()
    sub_frame_cheap = sub_frame[sub_frame['area'].isin(cheapest_boroughs)]
    sub_frame_expensive = sub_frame[sub_frame['area'].isin(expensive_boroughs)]
    plt.figure(figsize=(12, 10))
    sns.lineplot(data=sub_frame_cheap, x='date', y='mean_house_price', hue='area')
    plt.xticks(rotation=45)
    plt.legend(loc='upper left')
    plot_data('Monthly Mean House Price for the ten Cheapest Boroughs', 'Date', 'Mean House Price [£]')
    plt.figure(figsize=(12, 10))
    sns.lineplot(data=sub_frame_expensive, x='date', y='mean_house_price', hue='area')
    plt.xticks(rotation=45)
    plt.legend(loc='upper left')
    plot_data('Monthly Mean House Price for the ten most Expensive Boroughs', 'Date', 'Mean House Price [£]')

    # Plotting the gross annual pay per borough
    sns.set_style('whitegrid')
    data_frames['gross_annual_pay']['area_name'] = [area[:12] + '..' if len(area) > 12 else area for area in
                                                    data_frames['gross_annual_pay']['area_name']]
    plt.figure(figsize=(12, 12))
    sns.barplot(data=data_frames['gross_annual_pay'], x='area_name', y='gross_annual_pay')
    plt.xticks(rotation=45)
    plt.ylim(22500, 45000)
    plot_data('Gross Annual Pay per Borough', 'Borough', 'Gross Annual Pay [£]')

    # Health Indicators and Demographics

    # Life expectancy vs population density or proportion of population over 65
    sns.set_style('whitegrid')
    data_frames['health']['area_name'] = [area[:12] + '..' if len(area) > 12 else area for area in
                                          data_frames['health']['area_name']]
    sns.pairplot(data=data_frames['health'], x_vars=['male_life_expectancy'],
                 y_vars=['population_density', 'prop_population_over_65'], height=7, aspect=1.5,
                 plot_kws={'s': 100})
    plt.subplots_adjust(hspace=0.1)
    # title = 'Male Life Expectancy vs Population Density or Proportion of Population over 65'
    plt.savefig(os.path.join('../data/plots/', 'Male Life Expectancy vs Population Density or Proportion of '
                                               'Population over 65'.replace(' ', '_') + '.png'))
    sns.pairplot(data=data_frames['health'], x_vars=['female_life_expectancy'],
                 y_vars=['population_density', 'prop_population_over_65'], height=7, aspect=1.5,
                 plot_kws={'s': 100})
    plt.subplots_adjust(hspace=0.1)
    # title = 'Female Life Expectancy vs Population Density or Proportion of Population over 65'
    plt.savefig(os.path.join('../data/plots/', 'Female Life Expectancy vs Population Density or Proportion of '
                                               'Population over 65'.replace(' ', '_') + '.png'))

    # Education and Socio-Economic Factors

    # Proportion of working age population with no qualifications vs proportion of working age population with a degree
    sns.set_style('whitegrid')
    data_frames['education']['area_name'] = [area[:12] + '..' if len(area) > 12 else area for area in
                                             data_frames['education']['area_name']]
    sub_frame = data_frames['education'][['area_name', 'prop_working_age_no_qualif', 'prop_working_age_degree']]
    sub_frame.set_index('area_name', inplace=True)
    sub_frame.plot(kind='bar', stacked=True, figsize=(12, 12))
    plt.xticks(rotation=45)
    plot_data('Proportion of Working Age Population with No Qualifications vs Population with a Degree per Borough',
              'Borough', 'Education Attainment Levels [%]')

    # Correlation between GCSE results, income estimates and employment rates
    sns.set_style('whitegrid')
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        data_frames['education'][['achvmt_5_or_more_gcse', 'gross_annual_pay', 'employment_rate']].corr(),
        annot=True, cmap='Spectral', vmin=-1, vmax=1, center=0, linewidths=.5
    )
    plt.yticks(rotation=90)
    plot_data('Correlation between GCSE Results, Income Estimates [£] and Employment Rates [%]')

    # Transport and Environmental Analysis

    # Distribution of number of cars per household

    # Remove London from the data because it is a summary of all boroughs
    sns.set_style('whitegrid')
    data_frames['transport_env']['area_name'] = [area[:12] + '..' if len(area) > 12 else area for area in
                                                 data_frames['transport_env']['area_name']]
    transport_df = data_frames['transport_env'][data_frames['transport_env']['area_name'] != 'London']
    plt.figure(figsize=(12, 12))
    sns.barplot(data=transport_df, x='area_name', y='number_of_cars')
    plt.xticks(rotation=45)
    plt.grid(True)
    plot_data('Distribution of Number of Cars per Borough', 'Borough', 'Number of Cars [#]')

    # Public transport accessibility vs proportion of area that is greenspace
    sns.set_style('whitegrid')
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=data_frames['transport_env'], x='avg_public_transport_accessibility', y='pctg_area_greenspace',
                    s=100)
    for i, area in enumerate(data_frames['transport_env']['area_name']):
        plt.text(data_frames['transport_env']['avg_public_transport_accessibility'][i] + 0.05,
                 data_frames['transport_env']['pctg_area_greenspace'][i] + 0.25, area)
    plt.grid(True)
    plot_data('Average Public Transport Accessibility vs Proportion of Area that is Greenspace',
              'Average Public Transport Accessibility [#]', 'Proportion of Area that is Greenspace [%]')

    # Political Analysis

    # Plotting the proportion of seats won by each party in 2014 local elections
    sns.set_style('whitegrid')
    data_frames['political_analysis']['area_name'] = [area[:12] + '..' if len(area) > 12 else area for area in
                                                      data_frames['political_analysis']['area_name']]
    sub_frame = data_frames['political_analysis'][
        ['area_name', 'prop_seats_conservatives_2014_elect', 'prop_seats_labour_2014_elect',
         'prop_seats_lib_dems_2014_elect']]
    sub_frame.set_index('area_name', inplace=True)
    sub_frame.plot(kind='bar', stacked=True, figsize=(12, 12))
    plt.xticks(rotation=45)
    plt.legend(loc='upper right')
    plot_data('Proportion of Seats Won by each Party in 2014 Local Elections per Borough', 'Borough',
              'Proportion of Seats [%]')

    # Comparative analysis of turnout in 2014 local elections
    sns.set_style('whitegrid')
    data_frames['political_turnout']['area_name'] = [area[:12] + '..' if len(area) > 12 else area for area in
                                                     data_frames['political_turnout']['area_name']]
    plt.figure(figsize=(12, 8))
    sns.barplot(data=data_frames['political_turnout'], x='turnout_2014_local_elect', y='area_name')
    plt.xlim(20, 50)
    plot_data('Comparative Analysis of Turnout in 2014 Local Elections per Borough', 'Turnout [%]', 'Borough')

    # Wellbeing Analysis

    # Plotting the wellbeing scores per borough
    sns.set_style('whitegrid')
    data_frames['wellbeing_scores']['area_name'] = [area[:12] + '..' if len(area) > 12 else area for area in
                                                    data_frames['wellbeing_scores']['area_name']]
    sub_frame = data_frames['wellbeing_scores'][['area_name', 'life_satisfaction_score', 'happiness_score',
                                                 'anxiety_score', 'worthwhileness_score']]
    boroughs = sub_frame['area_name']
    num_boroughs = len(boroughs)
    fig, axs = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    color = sns.color_palette(palette='Pastel1')
    plot_radar(num_boroughs, axs, sub_frame['life_satisfaction_score'], 'Life Satisfaction [#]', 0.5, color[0])
    plot_radar(num_boroughs, axs, sub_frame['happiness_score'], 'Happiness [#]', 0.5, color[1])
    plot_radar(num_boroughs, axs, sub_frame['worthwhileness_score'], 'Worthwhileness [#]', 0.5, color[2])
    axs.set_xticks(np.linspace(0, 2 * np.pi, num_boroughs, endpoint=False))
    axs.set_xticklabels(boroughs)
    axs.set_ylim(6.8, 7.9)
    axs.set_rlabel_position(90)
    axs.legend(loc='upper right', bbox_to_anchor=(1, 1.1))
    title = 'Wellbeing Scores per Borough'
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join('../data/plots/', plt.gca().get_title().replace(' ', '_') + '.png'))

    # Plotting the wellbeing scores including anxiety per borough
    fig, axs = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    plot_radar(num_boroughs, axs, sub_frame['anxiety_score'], 'Anxiety [#]', 0.5, color[3])
    axs.set_xticks(np.linspace(0, 2 * np.pi, num_boroughs, endpoint=False))
    axs.set_xticklabels(boroughs)
    axs.set_ylim(2.5, 3.8)
    axs.set_rlabel_position(90)
    axs.legend(loc='upper right', bbox_to_anchor=(1, 1.1))
    title = 'Wellbeing Scores including Anxiety per Borough'
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join('../data/plots/', plt.gca().get_title().replace(' ', '_') + '.png'))


if __name__ == "__main__":
    main()
