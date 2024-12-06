import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load dataset
def load_dataset(filepath):
    """
    Load Dataset
    Input: - Filepath
    Output: - pandas dataframe
    """
    df = pd.read_csv(filepath)
    df = df[~df['Season Number'].isin([16])]  # Insufficient data
    return df

# Plot 1: Deal success rate by industry
def plot_deal_success_rate(df):
    """
    A bar chart for deal success rate by industry.
    """
    deal_by_industry = df.groupby('Industry')['Got Deal'].mean().sort_values() * 100
    fig = px.bar(deal_by_industry, x=deal_by_industry.index, y=deal_by_industry.values,
                 labels={'x': 'Industry', 'y': 'Success Rate (in %)'},
                 title='Deal Success Rate by Industry')
    return fig

# Plot 2: Investment distribution by industry
def plot_investment_distribution(df):
    """
    A pie chart for investment distribution by industry.
    """
    investment_by_industry = df.groupby('Industry')['Total Deal Amount'].sum().reset_index()
    # import pdb;pdb.set_trace()
    fig = px.pie(investment_by_industry, names='Industry', values='Total Deal Amount',
                 title="Investment Distribution by Industry")
    fig.update_traces(textinfo='label+percent', textposition='inside', insidetextorientation='auto')
    return fig

# Plot 3: Average investment amount per industry
def plot_avg_investment(df):
    """
    A bar chart for the average investment amount per industry.
    """
    avg_investment = df.groupby(['Industry'])['Total Deal Amount'].mean().sort_values(ascending=False) / 1000000
    fig = px.bar(avg_investment, title='Avg. Investment Amount in Startup',
                 labels={'value': 'Investment (M)'})
    fig.update_layout(showlegend=False)
    return fig

# Plot 4: Geographic distribution of pitchers
def plot_geographic_distribution(df):
    """
    A choropleth map showing the geographic distribution of pitchers across United State. 
    """
    pitchers_per_state = df.groupby(['Pitchers State'])['Got Deal'].count().reset_index()
    fig = px.choropleth(pitchers_per_state, locations="Pitchers State", locationmode="USA-states",
                        color="Got Deal", color_continuous_scale="Viridis", scope="usa",
                        title="Geographic Distribution of Pitchers")
    return fig

# Plot 5: State trends in entrepreneurship
def plot_state_trends(df):
    """
    A bar chart showing state trends in entrepreneurship.
    """
    regional_trends = df.groupby(['Pitchers State', 'Industry'])['Total Deal Amount'].sum().unstack(fill_value=0)
    # import pdb;pdb.set_trace()
    regional_trends['Total Investment'] = regional_trends.sum(axis=1)
    sorted_df = regional_trends.sort_values(by='Total Investment', ascending=False).drop(columns={'Total Investment'})
    fig = px.bar(sorted_df[:5], title="State Trends in Entrepreneurship",
                 labels={'value': 'Total Investment ($)', 'Region': 'Region'})
    return fig

# Plot 6: Successful deals by industry and gender
def plot_gender_deal_success(df):
    """
    A bar chart for successful deals by industry and pitcher gender.
    """
    gender_deal_success = df.groupby(['Industry', 'Pitchers Gender'])['Got Deal'].sum().reset_index()
    fig = px.bar(gender_deal_success, x='Industry', y='Got Deal', color='Pitchers Gender',
                 barmode='group', title='Successful Deals by Industry and Pitchers Gender',
                 labels={'Got Deal': 'Successful Deals'})
    return fig

# Plot 7: Average investment by industry and gender
def plot_gender_investment(df):
    """
    A bar chart for average investment amount by industry and gender.
    """
    gender_investment = df.groupby(['Industry', 'Pitchers Gender'])['Total Deal Amount'].mean().reset_index()
    fig = px.bar(gender_investment, x='Industry', y='Total Deal Amount', color='Pitchers Gender',
                 barmode='group', title='Avg. Investment Amount by Industry and Pitchers Gender',
                 labels={'Total Deal Amount': 'Investment Amount (in $)'})
    return fig

# Plot 8: Investment distribution among sharks
def plot_shark_investment(df):
    """
    A pie chart showing investment distribution among sharks.
    """
    shark_columns = ['Barbara Corcoran Investment Amount', 'Mark Cuban Investment Amount', 'Lori Greiner Investment Amount', 'Robert Herjavec Investment Amount', 'Daymond John Investment Amount', 'Kevin O Leary Investment Amount'] 

    shark_investments = df[shark_columns].sum().reset_index()
    shark_investments.columns = ['Shark', 'Investment Amount']
    # import pdb;pdb.set_trace()
    shark_investments['Percentage'] = (shark_investments['Investment Amount'] / shark_investments['Investment Amount'].sum()) * 100
    shark_investments['Shark'] = shark_investments['Shark'].str.replace(' Investment Amount', '')

    fig = px.pie(shark_investments, names='Shark', values='Percentage', title="Investment Distribution Among Sharks")
    fig.update_traces(textinfo='label+percent', textposition='inside' ,insidetextorientation='auto')
    return fig

# Plot 9: Sankey diagram for deal flow
def plot_sankey_deal_flow(df, sharks=None, industries=None, title=None):
    """
    A Sankey diagram for deal flow from industries to sharks.
    """
    industries = industries or df['Industry'].unique()
    sharks = sharks or ['Barbara Corcoran', 'Mark Cuban', 'Lori Greiner', 'Robert Herjavec', 'Daymond John', 'Kevin O Leary']
    title = title or "Deal Flow from Industries to Sharks"

    sources, targets, values = [], [], []
    # import pdb;pdb.set_trace()
    for industry in industries:
        industry_data = df[df['Industry'] == industry]
        for shark in sharks:
            total_investment = industry_data[f'{shark} Investment Amount'].sum()
            if total_investment > 0:
                sources.append(list(industries).index(industry))
                targets.append(len(industries) + sharks.index(shark))
                values.append(total_investment)

    fig = go.Figure(go.Sankey(
        node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=list(industries) + sharks),
        link=dict(source=sources, target=targets, value=values)))
    fig.update_layout(title_text=title, font_size=10)
    return fig

# Plot 10: Scatter plot of vierwership vs deal success rate for industries
def plot_scatter_views_deal_success(df):
    """
    A Scatter plot of vierwership vs deal success rate for industries.
    """

    #Calculate vierwership & deal success rate for each industry
    result_sum = df.groupby('Industry')[['Got Deal', 'US Viewership']].sum().reset_index()
    industry_count = df['Industry'].value_counts().reset_index()
    industry_count.columns = ['Industry', 'Count']
    final_result = pd.merge(result_sum, industry_count, on='Industry', how='outer')
    final_result['success rate'] = final_result['Got Deal'] / final_result['Count'] * 100
    final_result['avg views'] = final_result['US Viewership'] / final_result['Count']
    final_result = final_result[final_result['Industry'] != 'Uncertain/Other']

    #Generate scatter plot
    fig = px.scatter(
        final_result,
        x='avg views',
        y='success rate',
        hover_name='Industry',
        text='Industry',
        title='US Viewership vs Success Rate by Industry',
        labels={'avg views': 'Average US Viewership (in million)', 'success rate': 'Success Rate (%)'},
        color_discrete_sequence=['blue']
    )

    fig.update_traces(
        textposition='top center',
        textfont=dict(size=20),
        marker=dict(opacity=0.7)
    )

    fig.update_layout(
        width=1800,
        height=1200,
        xaxis=dict(
            title_font=dict(size=20), 
            tickfont=dict(size=12),
            dtick=400,
            range=[4, max(final_result['avg views']) + 0.1]
        ),
        yaxis=dict(title_font=dict(size=20), tickfont=dict(size=12)),
        title=dict(font=dict(size=20)),
        hovermode='closest',
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig

# Plot 11: Pie chart gender of all pithchers and successful pitchers
def plot_pie_gender(df):
    """
    A Pie chart gender of all pithchers and successful pitchers
    """
    #Successful pitchers
    deals_made = df[df['Got Deal'] == 1]
    gender_percentages = deals_made['Pitchers Gender'].value_counts(normalize=True) * 100
    fig_successful = px.pie(
        names=gender_percentages.index,
        values=gender_percentages.values,
        title='Gender Distribution of Successful Pitchers',
        labels={'label': 'Gender', 'value': 'Percentage'}
    )
    fig_successful.update_traces(textinfo='percent+label', textfont_size=20)
    fig_successful.update_layout(title_font_size=20)
    
    #Overall pitchers
    gender_counts = df['Pitchers Gender'].value_counts()
    fig_overall = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        title='Gender Distribution of Pitchers',
        labels={'label': 'Gender', 'value': 'Count'}
    )
    fig_overall.update_traces(textinfo='percent+label', textfont_size=20)
    fig_overall.update_layout(title_font_size=20)
    
    return fig_successful, fig_overall

# Plot 12: Stacked bar chart to show the gender diversity of pitchers across seasons
def plot_stackedbar_gender(df):
    """
    A Stacked bar chart to show the gender percentage of pitchers across seasons
    """

    # Calculate gender diversity percentages by season
    data = df.loc[df['Season Number'] != 16]
    gender_data = data[['Season Number', 'Pitchers Gender']]
    gender_counts = gender_data.groupby(['Season Number', 'Pitchers Gender']).size().unstack(fill_value=0)
    gender_percentage = gender_counts.div(gender_counts.sum(axis=1), axis=0) * 100

    custom_colors = {
        'Male': '#1f77b4',    
        'Female': '#ff7f0e',  
        'Mixed Team': '#2ca02c'    
    }

    # Create the stacked bar graph
    fig = go.Figure()

    for gender in gender_percentage.columns:
        fig.add_trace(go.Bar(
            x=gender_percentage.index,
            y=gender_percentage[gender],
            name=gender,
            text=gender_percentage[gender].round(1),
            textposition='inside',
            marker=dict(color=custom_colors.get(gender, '#d3d3d3'))  # Use custom colors
        ))

    fig.update_layout(
        title={
            'text': 'Gender Diversity in Shark Tank Pitches by Season',
            'font': {'size': 24}
        },
        xaxis={
            'title': {'text': 'Season Number', 'font': {'size': 18}},
            'tickfont': {'size': 14}
        },
        yaxis={
            'title': {'text': 'Percentage', 'font': {'size': 18}},
            'tickfont': {'size': 14}
        },
        legend={
            'title': {'text': 'Pitchers Gender', 'font': {'size': 16}},
            'font': {'size': 14}
        },
        barmode='stack',
        template='plotly',
        margin=dict(t=50, b=50, l=50, r=50)
    )

    return fig



# Example usage
if __name__ == "__main__":
    filepath = 'Shark Tank US dataset.csv'
    df = load_dataset(filepath)

    # Generate plots
    fig1 = plot_deal_success_rate(df)
    fig2 = plot_investment_distribution(df)
    fig3 = plot_avg_investment(df)
    fig4 = plot_geographic_distribution(df)
    fig5 = plot_state_trends(df)
    fig6 = plot_gender_deal_success(df)
    fig7 = plot_gender_investment(df)
    fig8 = plot_shark_investment(df)
    fig9 = plot_sankey_deal_flow(df)
    fig10 = plot_sankey_deal_flow(df,sharks=['Mark Cuban'],title='Mark Cuban Deal Flow to Industries')
    fig11 = plot_sankey_deal_flow(df,industries=['Media/Entertainment','Pet Products'],title='Deal Flow from Fashion/Beauty to Sharks')
    fig12 = plot_scatter_views_deal_success(df)
    fig13, fig14  = plot_pie_gender(df)
    fig15 = plot_stackedbar_gender(df)

    # Show example plot
    # fig1.show()
    # fig2.show()
    # fig3.show()
    # fig4.show()
    # fig5.show()
    # fig6.show()
    # fig7.show()
    # fig8.show()
    # fig9.show()
    # fig10.show()
    # fig11.show()
    # fig12.show()
    # fig13.show()
    # fig14.show()
    # fig15.show()