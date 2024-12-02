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