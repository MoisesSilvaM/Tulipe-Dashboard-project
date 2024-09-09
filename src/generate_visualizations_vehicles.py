import plotly.express as px
import plotly.graph_objects as go


def generate_visualizations(vehicle_data_without, vehicle_data_with, vehicle, veh_traffic):
    traffic_indicator = "tripinfo_" + vehicle
    vehicle_data_without = vehicle_data_without.loc[:,
         ['tripinfo_id',
          traffic_indicator]]
    vehicle_data_with = vehicle_data_with.loc[:,
         ['tripinfo_id',
          traffic_indicator]]
    fig1 = generate_figure1(vehicle_data_without, vehicle_data_with, veh_traffic, traffic_indicator)
    return fig1


def generate_figure1(vehicle_data_without, vehicle_data_with, veh_traffic, traffic_indicator):
    fig1 = go.Figure()
    fig1.add_trace(go.Histogram(x=vehicle_data_without[traffic_indicator], name="Without deviations"))
    fig1.add_trace(go.Histogram(x=vehicle_data_with[traffic_indicator], name="With deviations"))
    fig1.update_layout(
        title_text='Frequency distribution of the results obtained by the vehicles in terms of<br>' + veh_traffic + 'for the whole simulation',
        # title of plot
        xaxis_title_text=veh_traffic,  # xaxis label
        yaxis_title_text='Number of vehicles',  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1  # gap between bars of the same location coordinates
    )
    fig1.update_layout(template='plotly_dark', font=dict(color='#deb522'))
    return fig1


def generate_figure2(vehicle_data_without, vehicle_data_with, traffic, traffic_indicator):
    vehicle_data_without['id'] = vehicle_data_without['tripinfo_id']
    vehicle_data_without['id'] = vehicle_data_without['id'].astype(str)
    vehicle_data_without = vehicle_data_without.set_index('tripinfo_id')
    vehicle_data_with = vehicle_data_with.set_index('tripinfo_id')
    df = vehicle_data_without.merge(vehicle_data_with, left_index=True, right_index=True, how="left")
    value_x = traffic_indicator + '_x'
    value_y = traffic_indicator + '_y'

    df['diff'] = df[value_y].sub(df[value_x], axis=0)
    df["diff"] = df["diff"].fillna(value=0)
    df[value_x] = df[value_x].fillna(value=0)
    df[value_y] = df[value_y].fillna(value=0)

    df = df.sort_values(by=['diff'], ascending=False).head(15)
    value = ''
    if traffic == 'duration':
        value = 'duration (s)'
    if traffic == 'timeLoss':
        value = 'time loss (s)'
    if traffic == 'waitingTime':
        value = 'waiting time (s)'
    fig2 = px.bar(df, y='diff', x='id', orientation='v',
                  color='diff', text='diff',
                  title='15 most impacted vehicles in terms of ' + value + ' comparing with and without deviations',
                  labels={'id': 'Id of the vehicles', 'diff': 'Difference in seconds'}
                  )
    if traffic == 'routeLength':
        value = 'route length (m)'
        fig2 = px.bar(df, y='diff', x='id', orientation='v',
                      color='diff', text='diff',
                      title='15 most impacted vehicles in terms of ' + value + ' comparing with and without deviations',
                      labels={'id': 'Id of the vehicles', 'diff': 'Difference in meters'}
                      )

    fig2.update_traces(texttemplate='%{text}(s)', textposition='outside')
    if traffic == 'routeLength':
        fig2.update_traces(texttemplate='%{text}(m)', textposition='outside')
    fig2.update_layout(yaxis=dict(categoryorder='total ascending'))
    fig2.update_layout(template='plotly_dark', font=dict(color='#deb522'))
    return fig2
