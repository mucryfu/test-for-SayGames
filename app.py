import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

st.title('Helicopter Escape 3d Analytics Demo')

with st.sidebar:
    st.markdown('[Retention of the 1 and 7 days](#retention-of-the-1-and-7-days)')
    st.markdown('[Loserate by levels](#loserate-by-levels)')
    st.markdown('[The number of players who left by level](#the-number-of-players-who-left-by-level)')
    st.markdown('[Average level duration](#average-level-duration)')
    st.markdown('[Average session duration](#average-session-duration)')
    st.markdown('[Popularity of guns](#popularity-of-guns)')



st.header('Introduction')
st.markdown('''In the test visualization, the number of levels in sections with aggregation is limited to 20. However, in the queries used for exporting data used in the visualization, this limitation was not applied. 

To view or hide the query code, click on the `"Show Query Code"` button :)''')

# Ретенш 1 и 7 дней

st.header('Retention of the 1 and 7 days')
st.subheader('Total')
df_r = pd.read_csv('data/retention_count_total_users_202307221802.csv')
df_r_all = df_r.groupby(by=['retention_days']).sum()
df_r_all['retention_percent'] = df_r_all['retention_count'] / df_r_all['total_users'] * 100

fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'indicator'}, {'type': 'indicator'}]])

fig.add_trace(go.Indicator(
    mode = "gauge+number+delta",
    value = df_r_all['retention_percent'][1],
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {
        'axis': {'range': [None, 100]},
        'bar': {'color': "lightgreen"}
    },
    number = {'suffix': "%"},
    title = {'text': "One day retention"}
), row=1, col=1)

fig.add_trace(go.Indicator(
    mode = "gauge+number+delta",
    value = df_r_all['retention_percent'][7],
    domain = {'x': [0, 1], 'y': [0, 1]},
    gauge = {
        'axis': {'range': [None, 100]},
        'bar': {'color': "lightgreen"}
    },
    number = {'suffix': "%"},
    title = {'text': "Seven day retention"}
), row=1, col=2)

st.plotly_chart(fig, use_container_width=True)


st.subheader('Group by country')
options_1 = st.multiselect(
    'Group by country',
    ['IN', 'US', 'RU', 'MX', 'BR', 'LR', 'IS', 'LA', 'SO', 'VN', 'BJ', 'FJ', 'KY', 'DZ', 'TW', 'TM', 'EH', 'TD', 'MZ', 'BY', 'GB', 'VG', 'HR', 'IT', 'CV', 'RS', 'LU', 'HU', 'BW', 'MT', 'SR', 'XX', 'VI', 'GL', 'MN', 'BD', 'SA', 'MG', 'GE', 'TC', 'JE', 'OM', 'TJ', 'NE', 'ZA', 'AF', 'NL', 'AO', 'PY', 'KW', 'AU', 'AR', 'BM', 'XK', 'FM', 'CL', 'MS', 'KM', 'PM', 'WF', 'AI', 'PL', 'PW', 'NC', 'PE', 'AS', 'NP', 'AZ', 'JP', 'ES', 'TL', 'GY', 'GP', 'MR', 'ST', 'VU', 'SG', 'YE', 'MA', 'BB', 'MH', 'SN', 'RO', 'FK', 'CY', 'CM', 'CD', 'CW', 'WS', 'LT', 'HT', 'SS', 'GW', 'MU', 'SZ', 'HN', 'BL', 'SI', 'MO', 'GM', 'BE', 'GD', 'ET', 'EG', 'JM', 'AG', 'KE', 'DO', 'PK', 'UY', 'AT', 'TV', 'IR', 'LS', 'LI', 'MF', 'IM', 'CO', 'CF', 'ID', 'LV', 'GU', 'MW', 'BT', 'SX', 'SK', 'MM', 'BN', 'GF', 'MD', 'SB', 'BG', 'VC', 'TZ', 'EE', 'QA', 'JO', 'UA', 'AE', 'KG', 'KN', 'AL', 'NO', 'DM', 'PS', 'DJ', 'KI', 'PG', 'PT', 'KZ', 'TT', 'TN', 'TG', 'BZ', 'MY', 'SE', 'GA', 'BS', 'GR', 'MP', 'SV', 'YT', 'HK', 'BI', 'GH', 'SL', 'CA', 'LB', 'CH', 'LK', 'FI', 'CR', 'RW', 'NF', 'AX', 'MC', 'AW', 'PR', 'UZ', 'AD', 'NG', 'DE', 'PA', 'AM', 'PH', 'TH', 'TR', 'SC', 'ME', 'GG', 'BF', 'GN', 'ML', 'BO', 'SY', 'MV', 'GT', 'IE', 'CG', 'FO', 'CN', 'IL', 'IQ', 'FR', 'CZ', 'LY', 'CI', 'RE', 'LC', 'BH', 'GI', 'MK', 'BA', 'VE', 'SD', 'MQ', 'EC', 'NZ', 'ZW', 'KR', 'PF', 'UG', 'DK', 'NI', 'ZM', 'KH', 'SM'],
    ['IN', 'US', 'RU', 'MX', 'BR'])

df_r_1 = df_r.loc[df_r['retention_days'] == 1]
df_r_7 = df_r.loc[df_r['retention_days'] == 7]

def make_fig(df, countries=['IN', 'US', 'RU', 'MX', 'BR'], name=''):
    df = df[df['country'].isin(countries)]
    df = df.sort_values('retention_percent', ascending=False)

    colors = ['lightgreen']
    fig = px.bar(df, x='country', y='retention_percent', color_discrete_sequence=colors)
    fig.update_layout(
        title=name,
        xaxis_title='Country',
        yaxis_title='Retention Percent',
        yaxis=dict(range=[0, 100])
    )
    return fig

fig_1 = make_fig(df_r_1, countries=options_1, name='One day retention')
fig_2 = make_fig(df_r_7, countries=options_1, name='Seven Day retention')

st.plotly_chart(fig_1, use_container_width=True)
st.plotly_chart(fig_2, use_container_width=True)

code_1 = '''-- Создание общей таблицы событий с информацией о стране
WITH events_with_country AS (
    -- Выборка столбцов device_id, session, server_date из таблицы test.events и столбца country из таблицы test.devices
    SELECT events.device_id, events.session, events.server_date, devices.country
    -- Объединение таблиц test.events и test.devices по device_id
    FROM test.events AS events
    JOIN test.devices AS devices ON events.device_id = devices.device_id
),
-- Создание таблицы с датой первой сессии для каждого устройства
first_session AS (
    -- Выборка столбцов device_id, минимальной даты server_date (первой сессии) и country из таблицы events_with_country
    SELECT device_id, MIN(server_date) AS first_session_date, country
    FROM events_with_country
    -- Группировка по device_id и country
    GROUP BY device_id, country
),
-- Создание таблицы удержания пользователей
retention AS (
    -- Выборка столбцов device_id, first_session_date, country из таблицы first_session и server_date из таблицы events_with_country,
    -- а также разницы в днях между first_session_date и server_date как retention_days
    SELECT 
        first_session.device_id,
        first_session.first_session_date,
        first_session.country,
        events_with_country.server_date,
        dateDiff('day', first_session.first_session_date, events_with_country.server_date) AS retention_days
    FROM 
        first_session
        -- Объединение таблиц first_session и events_with_country по device_id
        JOIN events_with_country ON first_session.device_id = events_with_country.device_id
),
-- Создание таблицы с количеством удержанных пользователей для 1-го и 7-го дня удержания
retention_count AS (
    -- Выборка столбцов country, retention_days и количества уникальных device_id как retention_count из таблицы retention
    SELECT country, retention_days, COUNT(DISTINCT device_id) AS retention_count
    FROM retention
    -- Фильтрация строк с retention_days равным 1 или 7
    WHERE retention_days IN (1, 7)
    -- Группировка по country и retention_days
    GROUP BY country, retention_days
),
-- Создание таблицы с общим количеством пользователей для каждой страны
total_users AS (
    -- Выборка столбцов country и количества уникальных device_id как total_users из таблицы first_session
    SELECT country, COUNT(DISTINCT device_id) AS total_users FROM first_session GROUP BY country
)
-- Выборка столбцов country, retention_days из таблицы retention_count,
-- total_users из таблицы total_users,
-- retention_count из таблицы retention_count,
-- а также процента удержания как (retention_count * 100.0) / total_users округленного до 2 знаков после запятой как retention_percent 
SELECT 
    retention_count.country,
    retention_count.retention_days,
    total_users.total_users,
    retention_count.retention_count,
    ROUND((retention_count.retention_count * 100.0) / total_users.total_users, 2) AS retention_percent
FROM 
    -- Объединение таблиц retention_count и total_users по country 
    retention_count
    JOIN total_users ON retention_count.country = total_users.country;'''

toggle_1 = st.checkbox('Show Query Code')

if toggle_1:
    st.code(code_1, language="sql", line_numbers=True)

else:
    st.write('')


# Лузрейт по уровням

st.header('Loserate by levels')

df_l = pd.read_csv('data/loserate.csv')
df_l = df_l.loc[(df_l['level'] != 194000) & (df_l['level'] != 1940010000)]

options_2 = st.multiselect(
    'Group by country',
    ['all', 'IN', 'US', 'RU', 'MX', 'BR', 'LR', 'IS', 'LA', 'SO', 'VN', 'BJ', 'FJ', 'KY', 'DZ', 'TW', 'TM', 'EH', 'TD', 'MZ', 'BY', 'GB', 'VG', 'HR', 'IT', 'CV', 'RS', 'LU', 'HU', 'BW', 'MT', 'SR', 'XX', 'VI', 'GL', 'MN', 'BD', 'SA', 'MG', 'GE', 'TC', 'JE', 'OM', 'TJ', 'NE', 'ZA', 'AF', 'NL', 'AO', 'PY', 'KW', 'AU', 'AR', 'BM', 'XK', 'FM', 'CL', 'MS', 'KM', 'PM', 'WF', 'AI', 'PL', 'PW', 'NC', 'PE', 'AS', 'NP', 'AZ', 'JP', 'ES', 'TL', 'GY', 'GP', 'MR', 'ST', 'VU', 'SG', 'YE', 'MA', 'BB', 'MH', 'SN', 'RO', 'FK', 'CY', 'CM', 'CD', 'CW', 'WS', 'LT', 'HT', 'SS', 'GW', 'MU', 'SZ', 'HN', 'BL', 'SI', 'MO', 'GM', 'BE', 'GD', 'ET', 'EG', 'JM', 'AG', 'KE', 'DO', 'PK', 'UY', 'AT', 'TV', 'IR', 'LS', 'LI', 'MF', 'IM', 'CO', 'CF', 'ID', 'LV', 'GU', 'MW', 'BT', 'SX', 'SK', 'MM', 'BN', 'GF', 'MD', 'SB', 'BG', 'VC', 'TZ', 'EE', 'QA', 'JO', 'UA', 'AE', 'KG', 'KN', 'AL', 'NO', 'DM', 'PS', 'DJ', 'KI', 'PG', 'PT', 'KZ', 'TT', 'TN', 'TG', 'BZ', 'MY', 'SE', 'GA', 'BS', 'GR', 'MP', 'SV', 'YT', 'HK', 'BI', 'GH', 'SL', 'CA', 'LB', 'CH', 'LK', 'FI', 'CR', 'RW', 'NF', 'AX', 'MC', 'AW', 'PR', 'UZ', 'AD', 'NG', 'DE', 'PA', 'AM', 'PH', 'TH', 'TR', 'SC', 'ME', 'GG', 'BF', 'GN', 'ML', 'BO', 'SY', 'MV', 'GT', 'IE', 'CG', 'FO', 'CN', 'IL', 'IQ', 'FR', 'CZ', 'LY', 'CI', 'RE', 'LC', 'BH', 'GI', 'MK', 'BA', 'VE', 'SD', 'MQ', 'EC', 'NZ', 'ZW', 'KR', 'PF', 'UG', 'DK', 'NI', 'ZM', 'KH', 'SM'],
    ['all'])

if len(options_2) > 1:
    try:
        options_2.remove('all')
    except:
        options_2 = options_2

level_min = st.number_input('Insert level', min_value=1, max_value=20, value=1)
lenel_max = st.number_input('to level', min_value=1, max_value=20, value=10)

df_l = df_l.loc[(df_l['level'] >= level_min) & (df_l['level'] <= lenel_max)]

if (len(options_2) == 1) & (options_2[0] == 'all'):
    df_l = df_l
else:
    df_l = df_l.loc[df_l['country'].isin(options_2)]

df_l_all = df_l.groupby(by='level').sum()
df_l_all['churn_rate'] = 100-(df_l_all['players_completed'] / df_l_all['players_started'] * 100)

N = len(df_l_all.index)
ind = np.arange(N)

fig = go.Figure()
fig.add_trace(go.Bar(x=ind, y=df_l_all['churn_rate'], name='Lose Rate', marker_color='lightcoral'))
fig.add_trace(go.Bar(x=ind, y=100 - df_l_all['churn_rate'], name='Retention Rate', marker_color='lightgreen'))

fig.update_layout(
title='Loserate by Level',
xaxis_title='Level',
yaxis_title='Loserate (%)',
barmode='stack',
width=800,
height=600
)


fig.update_xaxes(tickvals=ind, ticktext=df_l_all.index)

st.plotly_chart(fig)

code_2 = '''-- Создание таблицы с количеством игроков, начавших каждый уровень в каждой стране
WITH level_started AS (
    -- Выборка столбцов country из таблицы test.devices, level из таблицы test.events и количества уникальных device_id как players
    SELECT
        devices.country,
        events.level,
        COUNT(DISTINCT events.device_id) AS players
    -- Объединение таблиц test.events и test.devices по device_id
    FROM test.events AS events
    JOIN test.devices AS devices ON events.device_id = devices.device_id
    -- Фильтрация строк с event равным 'level_started'
    WHERE events.event = 'level_started'
    -- Группировка по country и level
    GROUP BY devices.country, events.level
),
-- Создание таблицы с количеством игроков, завершивших каждый уровень в каждой стране
level_completed AS (
    -- Выборка столбцов country из таблицы test.devices, level из таблицы test.events и количества уникальных device_id как players
    SELECT
        devices.country,
        events.level,
        COUNT(DISTINCT events.device_id) AS players
    -- Объединение таблиц test.events и test.devices по device_id
    FROM test.events AS events
    JOIN test.devices AS devices ON events.device_id = devices.device_id
    -- Фильтрация строк с event равным 'level_completed'
    WHERE events.event = 'level_completed'
    -- Группировка по country и level
    GROUP BY devices.country, events.level
)
-- Выборка столбцов country, level из таблицы level_started,
-- players из таблицы level_started как players_started,
-- players из таблицы level_completed как players_completed,
-- а также процента оттока как (players_started - players_completed) / players_started * 100 как churn_rate 
SELECT
    level_started.country,
    level_started.level,
    level_started.players AS players_started,
    level_completed.players AS players_completed,
    (level_started.players - level_completed.players) / level_started.players * 100 AS churn_rate
-- Объединение таблиц level_started и level_completed по country и level 
FROM level_started
JOIN level_completed ON level_started.country = level_completed.country AND level_started.level = level_completed.level
-- Сортировка по country и level 
ORDER BY level_started.country, level_started.level;'''

toggle_2 = st.checkbox('Show Query Code ')

if toggle_2:
    st.code(code_2, language="sql", line_numbers=True)

else:
    st.write('')


# The number of players who left by level

st.header('The number of players who left by level')

df_lu = pd.read_csv('data/lose_users.csv')

options_3 = st.multiselect(
    'Group by Country',
    ['all', 'IN', 'US', 'RU', 'MX', 'BR', 'LR', 'IS', 'LA', 'SO', 'VN', 'BJ', 'FJ', 'KY', 'DZ', 'TW', 'TM', 'EH', 'TD', 'MZ', 'BY', 'GB', 'VG', 'HR', 'IT', 'CV', 'RS', 'LU', 'HU', 'BW', 'MT', 'SR', 'XX', 'VI', 'GL', 'MN', 'BD', 'SA', 'MG', 'GE', 'TC', 'JE', 'OM', 'TJ', 'NE', 'ZA', 'AF', 'NL', 'AO', 'PY', 'KW', 'AU', 'AR', 'BM', 'XK', 'FM', 'CL', 'MS', 'KM', 'PM', 'WF', 'AI', 'PL', 'PW', 'NC', 'PE', 'AS', 'NP', 'AZ', 'JP', 'ES', 'TL', 'GY', 'GP', 'MR', 'ST', 'VU', 'SG', 'YE', 'MA', 'BB', 'MH', 'SN', 'RO', 'FK', 'CY', 'CM', 'CD', 'CW', 'WS', 'LT', 'HT', 'SS', 'GW', 'MU', 'SZ', 'HN', 'BL', 'SI', 'MO', 'GM', 'BE', 'GD', 'ET', 'EG', 'JM', 'AG', 'KE', 'DO', 'PK', 'UY', 'AT', 'TV', 'IR', 'LS', 'LI', 'MF', 'IM', 'CO', 'CF', 'ID', 'LV', 'GU', 'MW', 'BT', 'SX', 'SK', 'MM', 'BN', 'GF', 'MD', 'SB', 'BG', 'VC', 'TZ', 'EE', 'QA', 'JO', 'UA', 'AE', 'KG', 'KN', 'AL', 'NO', 'DM', 'PS', 'DJ', 'KI', 'PG', 'PT', 'KZ', 'TT', 'TN', 'TG', 'BZ', 'MY', 'SE', 'GA', 'BS', 'GR', 'MP', 'SV', 'YT', 'HK', 'BI', 'GH', 'SL', 'CA', 'LB', 'CH', 'LK', 'FI', 'CR', 'RW', 'NF', 'AX', 'MC', 'AW', 'PR', 'UZ', 'AD', 'NG', 'DE', 'PA', 'AM', 'PH', 'TH', 'TR', 'SC', 'ME', 'GG', 'BF', 'GN', 'ML', 'BO', 'SY', 'MV', 'GT', 'IE', 'CG', 'FO', 'CN', 'IL', 'IQ', 'FR', 'CZ', 'LY', 'CI', 'RE', 'LC', 'BH', 'GI', 'MK', 'BA', 'VE', 'SD', 'MQ', 'EC', 'NZ', 'ZW', 'KR', 'PF', 'UG', 'DK', 'NI', 'ZM', 'KH', 'SM'],
    ['all'])

if len(options_3) > 1:
    try:
        options_3.remove('all')
    except:
        options_3 = options_3

level_min_1 = st.number_input('Insert Level', min_value=1, max_value=20, value=1)
level_max_1 = st.number_input('to Level', min_value=1, max_value=20, value=10)

if (len(options_3) == 1) & (options_3[0] == 'all'):
    df_lu = df_lu
else:
    df_lu = df_lu.loc[df_lu['country'].isin(options_3)]

df_lu = df_lu.loc[(df_lu['level'] >= level_min_1) & (df_lu['level'] <= level_max_1)]

df_lu_all = df_lu.groupby('level').sum()
fig = px.bar(df_lu_all.reset_index(), x=['players_started', 'players_churned'], y='level', orientation='h', color_discrete_sequence=['lightgreen', 'lightcoral'])
fig.update_layout(yaxis=dict(autorange="reversed"), width=800,
height=600)
st.plotly_chart(fig)

code_3 = '''-- Объявление общего табличного выражения для подсчета количества игроков, которые начали уровень
WITH
    level_started AS (
        SELECT
            devices.country, -- Выбор страны
            events.level, -- Выбор уровня
            COUNT(DISTINCT events.device_id) AS players_started -- Подсчет количества уникальных игроков, которые начали уровень
        FROM test.events AS events -- Использование таблицы событий
        JOIN test.devices AS devices ON events.device_id = devices.device_id -- Присоединение таблицы устройств по идентификатору устройства
        WHERE events.event = 'level_started' -- Фильтрация событий, чтобы выбрать только те, которые соответствуют началу уровня
        GROUP BY devices.country, events.level -- Группировка по стране и уровню
    ),
    -- Объявление общего табличного выражения для подсчета количества игроков, которые завершили уровень
    level_completed AS (
        SELECT
            devices.country, -- Выбор страны
            events.level, -- Выбор уровня
            COUNT(DISTINCT events.device_id) AS players_completed -- Подсчет количества уникальных игроков, которые завершили уровень
        FROM test.events AS events -- Использование таблицы событий
        JOIN test.devices AS devices ON events.device_id = devices.device_id -- Присоединение таблицы устройств по идентификатору устройства
        WHERE events.event = 'level_completed' -- Фильтрация событий, чтобы выбрать только те, которые соответствуют завершению уровня
        GROUP BY devices.country, events.level -- Группировка по стране и уровню
    )
-- Выбор данных из общих табличных выражений и вычисление разницы между количеством игроков, которые начали и завершили уровень
SELECT
    level_started.country, -- Выбор страны из первого общего табличного выражения
    level_started.level, -- Выбор уровня из первого общего табличного выражения
    level_started.players_started, -- Выбор количества игроков, которые начали уровень из первого общего табличного выражения
    (level_started.players_started - level_completed.players_completed) AS players_churned -- Вычисление разницы между количеством игроков, которые начали и завершили уровень (отток игроков)
FROM level_started -- Использование первого общего табличного выражения в качестве основной таблицы для выборки данных
JOIN level_completed ON level_started.country = level_completed.country AND level_started.level = level_completed.level -- Присоединение второго общего табличного выражения по стране и уровню для получения соответствующих данных о завершении уровня
ORDER BY level_started.country, level_started.level; -- Упорядочивание результата по стране и уровню.'''

toggle_3 = st.checkbox('Show Query Code  ')

if toggle_3:
    st.code(code_3, language="sql", line_numbers=True)

else:
    st.write('')

# Средняя продолжительность уровня # Средняя продолжительность сессии
st.header('Average level duration and Average session duration')

left_column, right_column = st.columns(2)
def convert_time(seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f'{int(h):02d}:{int(m):02d}:{int(s):02d}'

with left_column:
    st.subheader('Average level duration')
    df_t = pd.read_csv('data/avg_dur_lev.csv')

    options_4 = st.multiselect(
        'Group By Country',
        ['all', 'IN', 'US', 'RU', 'MX', 'BR', 'LR', 'IS', 'LA', 'SO', 'VN', 'BJ', 'FJ', 'KY', 'DZ', 'TW', 'TM', 'EH', 'TD', 'MZ', 'BY', 'GB', 'VG', 'HR', 'IT', 'CV', 'RS', 'LU', 'HU', 'BW', 'MT', 'SR', 'XX', 'VI', 'GL', 'MN', 'BD', 'SA', 'MG', 'GE', 'TC', 'JE', 'OM', 'TJ', 'NE', 'ZA', 'AF', 'NL', 'AO', 'PY', 'KW', 'AU', 'AR', 'BM', 'XK', 'FM', 'CL', 'MS', 'KM', 'PM', 'WF', 'AI', 'PL', 'PW', 'NC', 'PE', 'AS', 'NP', 'AZ', 'JP', 'ES', 'TL', 'GY', 'GP', 'MR', 'ST', 'VU', 'SG', 'YE', 'MA', 'BB', 'MH', 'SN', 'RO', 'FK', 'CY', 'CM', 'CD', 'CW', 'WS', 'LT', 'HT', 'SS', 'GW', 'MU', 'SZ', 'HN', 'BL', 'SI', 'MO', 'GM', 'BE', 'GD', 'ET', 'EG', 'JM', 'AG', 'KE', 'DO', 'PK', 'UY', 'AT', 'TV', 'IR', 'LS', 'LI', 'MF', 'IM', 'CO', 'CF', 'ID', 'LV', 'GU', 'MW', 'BT', 'SX', 'SK', 'MM', 'BN', 'GF', 'MD', 'SB', 'BG', 'VC', 'TZ', 'EE', 'QA', 'JO', 'UA', 'AE', 'KG', 'KN', 'AL', 'NO', 'DM', 'PS', 'DJ', 'KI', 'PG', 'PT', 'KZ', 'TT', 'TN', 'TG', 'BZ', 'MY', 'SE', 'GA', 'BS', 'GR', 'MP', 'SV', 'YT', 'HK', 'BI', 'GH', 'SL', 'CA', 'LB', 'CH', 'LK', 'FI', 'CR', 'RW', 'NF', 'AX', 'MC', 'AW', 'PR', 'UZ', 'AD', 'NG', 'DE', 'PA', 'AM', 'PH', 'TH', 'TR', 'SC', 'ME', 'GG', 'BF', 'GN', 'ML', 'BO', 'SY', 'MV', 'GT', 'IE', 'CG', 'FO', 'CN', 'IL', 'IQ', 'FR', 'CZ', 'LY', 'CI', 'RE', 'LC', 'BH', 'GI', 'MK', 'BA', 'VE', 'SD', 'MQ', 'EC', 'NZ', 'ZW', 'KR', 'PF', 'UG', 'DK', 'NI', 'ZM', 'KH', 'SM'],
        ['all'])

    if len(options_4) > 1:
        try:
            options_4.remove('all')
        except:
            options_4 = options_4

    level_min_2 = st.number_input('Insert Level: ', min_value=1, max_value=20, value=1)
    level_max_2 = st.number_input('to Level: ', min_value=1, max_value=20, value=10)

    df_t = df_t.loc[(df_t['level'] >= level_min_2) & (df_t['level'] <= level_max_2)]

    if (len(options_4) == 1) & (options_4[0] == 'all'):
        df_t = df_t
        df_t = df_t.groupby('level').sum()
        df_t = df_t.reset_index()
        df_t['formatted_time'] = df_t['avg_duration'].apply(convert_time)
        df_t.rename(columns = {'formatted_time':' duration_time'}, inplace = True )
        df_t = df_t.drop('avg_duration', axis=1)
        df_t = df_t.drop('country', axis=1)
    else:
        df_t = df_t.loc[df_t['country'].isin(options_4)]
        df_t = df_t.groupby(['country', 'level']).sum()
        df_t['formatted_time'] = df_t['avg_duration'].apply(convert_time)
        df_t.rename(columns = {'formatted_time':' duration_time'}, inplace = True )
        df_t = df_t.drop('avg_duration', axis=1)

    st.dataframe(df_t)  

with right_column:
    st.subheader('Average session duration')
    df_s = pd.read_csv('data/avg_dur_sess.csv')

    options_5 = st.multiselect(
        'Group By Country ',
        ['all', 'IN', 'US', 'RU', 'MX', 'BR', 'LR', 'IS', 'LA', 'SO', 'VN', 'BJ', 'FJ', 'KY', 'DZ', 'TW', 'TM', 'EH', 'TD', 'MZ', 'BY', 'GB', 'VG', 'HR', 'IT', 'CV', 'RS', 'LU', 'HU', 'BW', 'MT', 'SR', 'XX', 'VI', 'GL', 'MN', 'BD', 'SA', 'MG', 'GE', 'TC', 'JE', 'OM', 'TJ', 'NE', 'ZA', 'AF', 'NL', 'AO', 'PY', 'KW', 'AU', 'AR', 'BM', 'XK', 'FM', 'CL', 'MS', 'KM', 'PM', 'WF', 'AI', 'PL', 'PW', 'NC', 'PE', 'AS', 'NP', 'AZ', 'JP', 'ES', 'TL', 'GY', 'GP', 'MR', 'ST', 'VU', 'SG', 'YE', 'MA', 'BB', 'MH', 'SN', 'RO', 'FK', 'CY', 'CM', 'CD', 'CW', 'WS', 'LT', 'HT', 'SS', 'GW', 'MU', 'SZ', 'HN', 'BL', 'SI', 'MO', 'GM', 'BE', 'GD', 'ET', 'EG', 'JM', 'AG', 'KE', 'DO', 'PK', 'UY', 'AT', 'TV', 'IR', 'LS', 'LI', 'MF', 'IM', 'CO', 'CF', 'ID', 'LV', 'GU', 'MW', 'BT', 'SX', 'SK', 'MM', 'BN', 'GF', 'MD', 'SB', 'BG', 'VC', 'TZ', 'EE', 'QA', 'JO', 'UA', 'AE', 'KG', 'KN', 'AL', 'NO', 'DM', 'PS', 'DJ', 'KI', 'PG', 'PT', 'KZ', 'TT', 'TN', 'TG', 'BZ', 'MY', 'SE', 'GA', 'BS', 'GR', 'MP', 'SV', 'YT', 'HK', 'BI', 'GH', 'SL', 'CA', 'LB', 'CH', 'LK', 'FI', 'CR', 'RW', 'NF', 'AX', 'MC', 'AW', 'PR', 'UZ', 'AD', 'NG', 'DE', 'PA', 'AM', 'PH', 'TH', 'TR', 'SC', 'ME', 'GG', 'BF', 'GN', 'ML', 'BO', 'SY', 'MV', 'GT', 'IE', 'CG', 'FO', 'CN', 'IL', 'IQ', 'FR', 'CZ', 'LY', 'CI', 'RE', 'LC', 'BH', 'GI', 'MK', 'BA', 'VE', 'SD', 'MQ', 'EC', 'NZ', 'ZW', 'KR', 'PF', 'UG', 'DK', 'NI', 'ZM', 'KH', 'SM'],
        ['all'])

    if len(options_5) > 1:
        try:
            options_5.remove('all')
        except:
            options_5 = options_5

    session_min = st.number_input('Insert session  ', min_value=1, max_value=20, value=1)
    session_max = st.number_input('to session  ', min_value=1, max_value=20, value=10)

    df_s = df_s.loc[(df_s['session_rank'] >= session_min) & (df_s['session_rank'] <= session_max)]

    if (len(options_5) == 1) & (options_5[0] == 'all'):
        df_s = df_s
        df_s = df_s.groupby('session_rank').sum()
        df_s = df_s.reset_index()
        df_s['formatted_time'] = df_s['avg_session_duration'].apply(convert_time)
        df_s.rename(columns = {'formatted_time':' duration_time'}, inplace = True )
        df_s = df_s.drop('avg_session_duration', axis=1)
        df_s = df_s.drop('country', axis=1)
    else:
        df_s = df_s.loc[df_s['country'].isin(options_4)]
        df_s = df_s.groupby(['country', 'session_rank']).sum()
        df_s['formatted_time'] = df_s['avg_session_duration'].apply(convert_time)
        df_s.rename(columns = {'formatted_time':' duration_time'}, inplace = True )
        df_s = df_s.drop('avg_session_duration', axis=1)

    st.dataframe(df_s)  

code_4 = '''-- Выбираем поля страны, уровня и средней продолжительности
SELECT
    devices.country,
    events.level,
    AVG(events.param1) AS avg_duration
-- Из таблицы событий
FROM test.events AS events
-- Соединяем с таблицей устройств по device_id
JOIN test.devices AS devices ON events.device_id = devices.device_id
-- Фильтруем только события завершения уровня
WHERE events.event = 'level_completed'
-- Группируем по стране и уровню
GROUP BY devices.country, events.level
-- Сортируем по стране и уровню
ORDER BY devices.country, events.level;'''

toggle_4 = st.checkbox('Show Query Code (average level duration)')

if toggle_4:
    st.code(code_4, language="sql", line_numbers=True)

else:
    st.write('')

code_5 = '''WITH
    session_durations AS (
        SELECT
            device_id,
            session,
            MAX(server_time) - MIN(server_time) AS session_duration
        FROM test.events
        GROUP BY device_id, session
    ),
    session_ranks AS (
        SELECT
            device_id,
            session,
            session_duration,
            rank() OVER (PARTITION BY device_id ORDER BY MIN(server_time)) AS session_rank
        FROM test.events
        JOIN session_durations USING (device_id, session)
        GROUP BY device_id, session, session_duration
    )
SELECT
    country,
    session_rank,
    AVG(session_duration) AS avg_session_duration
FROM test.devices
JOIN session_ranks USING (device_id)
GROUP BY country, session_rank;'''

toggle_5 = st.checkbox('Show Query Code (average session duration)')

if toggle_5:
    st.code(code_5, language="sql", line_numbers=True)

else:
    st.write('')

# Популярность пушек
st.header('Popularity of guns')
df_p = pd.read_csv('data/popul_guns.csv')

options_6 = st.multiselect(
        'Group By Country    ',
        ['all', 'IN', 'US', 'RU', 'MX', 'BR', 'LR', 'IS', 'LA', 'SO', 'VN', 'BJ', 'FJ', 'KY', 'DZ', 'TW', 'TM', 'EH', 'TD', 'MZ', 'BY', 'GB', 'VG', 'HR', 'IT', 'CV', 'RS', 'LU', 'HU', 'BW', 'MT', 'SR', 'XX', 'VI', 'GL', 'MN', 'BD', 'SA', 'MG', 'GE', 'TC', 'JE', 'OM', 'TJ', 'NE', 'ZA', 'AF', 'NL', 'AO', 'PY', 'KW', 'AU', 'AR', 'BM', 'XK', 'FM', 'CL', 'MS', 'KM', 'PM', 'WF', 'AI', 'PL', 'PW', 'NC', 'PE', 'AS', 'NP', 'AZ', 'JP', 'ES', 'TL', 'GY', 'GP', 'MR', 'ST', 'VU', 'SG', 'YE', 'MA', 'BB', 'MH', 'SN', 'RO', 'FK', 'CY', 'CM', 'CD', 'CW', 'WS', 'LT', 'HT', 'SS', 'GW', 'MU', 'SZ', 'HN', 'BL', 'SI', 'MO', 'GM', 'BE', 'GD', 'ET', 'EG', 'JM', 'AG', 'KE', 'DO', 'PK', 'UY', 'AT', 'TV', 'IR', 'LS', 'LI', 'MF', 'IM', 'CO', 'CF', 'ID', 'LV', 'GU', 'MW', 'BT', 'SX', 'SK', 'MM', 'BN', 'GF', 'MD', 'SB', 'BG', 'VC', 'TZ', 'EE', 'QA', 'JO', 'UA', 'AE', 'KG', 'KN', 'AL', 'NO', 'DM', 'PS', 'DJ', 'KI', 'PG', 'PT', 'KZ', 'TT', 'TN', 'TG', 'BZ', 'MY', 'SE', 'GA', 'BS', 'GR', 'MP', 'SV', 'YT', 'HK', 'BI', 'GH', 'SL', 'CA', 'LB', 'CH', 'LK', 'FI', 'CR', 'RW', 'NF', 'AX', 'MC', 'AW', 'PR', 'UZ', 'AD', 'NG', 'DE', 'PA', 'AM', 'PH', 'TH', 'TR', 'SC', 'ME', 'GG', 'BF', 'GN', 'ML', 'BO', 'SY', 'MV', 'GT', 'IE', 'CG', 'FO', 'CN', 'IL', 'IQ', 'FR', 'CZ', 'LY', 'CI', 'RE', 'LC', 'BH', 'GI', 'MK', 'BA', 'VE', 'SD', 'MQ', 'EC', 'NZ', 'ZW', 'KR', 'PF', 'UG', 'DK', 'NI', 'ZM', 'KH', 'SM'],
        ['all'])

if len(options_6) > 1:
    try:
        options_6.remove('all')
    except:
        options_6 = options_6

level_min_3 = st.number_input('Insert level    ', min_value=1, max_value=20, value=1)
level_max_3 = st.number_input('to level     ', min_value=1, max_value=20, value=10)

if (len(options_6) == 1) & (options_6[0] == 'all'):
    df_p = df_p
else:
    df_p = df_p.loc[df_p['country'].isin(options_6)]

df_p = df_p.loc[(df_p['level'] >= level_min_3) & (df_p['level'] <= level_max_3)]

option = st.selectbox(
    'Rating type',
    ('Top-1', 'Top-3', 'Top-5', 'Top-10'))

if option == 'Top-1':
    a = 1
if option == 'Top-3':
    a = 3
if option == 'Top-5':
    a = 5
if option == 'Top-10':
    a = 10



df_p['country'] = df_p['country'].astype(str)
df_p['level'] = df_p['level'].astype(int)
df_p['gun_name'] = df_p['gun_name'].astype(str)
df_p['users'] = df_p['users'].astype(int)
df_p['percentage'] = df_p['percentage'].astype(float)

df_p = df_p[['level', 'gun_name', 'percentage']]
df_p = df_p.groupby(['level', 'gun_name']).mean().reset_index()

df_p.rename(columns = {'percentage':'popularity'}, inplace = True )
# df_p = df_p.reset_index(drop=True)

# df_p = df_p.reset_index()
res = []
for i in df_p['level'].unique():
    df_buf = df_p.loc[df_p['level'] == i]
    df_buf = df_buf.sort_values(by='popularity', ascending=False).reset_index(drop=True)
    df_buf = df_buf[1:a+1]
    res.append(df_buf)
df = pd.concat(res)

st.dataframe(df)

code_6 = '''-- Создаем подзапрос gun_stats, который вычисляет количество пользователей, выбирающих каждый пистолет на каждом уровне в каждой стране
WITH gun_stats AS (
    SELECT
        country, -- Выбираем страну
        JSONExtractInt(extra, 'level_tnt') AS level, -- Извлекаем уровень из поля extra
        JSONExtractString(extra, 'gun_name') AS gun_name, -- Извлекаем имя пистолета из поля extra
        COUNT(DISTINCT device_id) AS users -- Считаем количество уникальных пользователей
    FROM test.events -- Используем таблицу test.events
    JOIN test.devices USING (device_id) -- Присоединяем таблицу test.devices по полю device_id
    WHERE event = 'level_started' -- Отбираем только события начала уровня
    GROUP BY country, level, gun_name -- Группируем результаты по стране, уровню и имени пистолета
),
-- Создаем подзапрос total_stats, который вычисляет общее количество пользователей на каждом уровне в каждой стране
total_stats AS (
    SELECT
        country, -- Выбираем страну
        JSONExtractInt(extra, 'level_tnt') AS level, -- Извлекаем уровень из поля extra
        COUNT(DISTINCT device_id) AS total_users -- Считаем общее количество уникальных пользователей
    FROM test.events -- Используем таблицу test.events
    JOIN test.devices USING (device_id) -- Присоединяем таблицу test.devices по полю device_id
    WHERE event = 'level_started' -- Отбираем только события начала уровня
    GROUP BY country, level -- Группируем результаты по стране и уровню
)
-- Выбираем результаты из подзапросов gun_stats и total_stats и вычисляем процент пользователей, выбирающих каждый пистолет на каждом уровне в каждой стране
SELECT
    gun_stats.country, -- Выбираем страну из подзапроса gun_stats
    gun_stats.level, -- Выбираем уровень из подзапроса gun_stats
    gun_stats.gun_name, -- Выбираем имя пистолета из подзапроса gun_stats
    gun_stats.users, -- Выбираем количество пользователей из подзапроса gun_stats
    gun_stats.users / total_stats.total_users * 100 AS percentage -- Вычисляем процент пользователей, выбирающих данный пистолет на данном уровне в данной стране
FROM gun_stats -- Используем результаты подзапроса gun_stats
JOIN total_stats USING (country, level) -- Присоединяем результаты подзапроса total_stats по полям country и level
ORDER BY country, level, percentage DESC; -- Сортируем результаты по стране, уровню и проценту в порядке убывания процента.'''

toggle_6 = st.checkbox('Show Query Code     ')

if toggle_6:
    st.code(code_6, language="sql", line_numbers=True)

else:
    st.write('')















