# Sleep Habits & Late-Night Screen Time Dashboard
## Live App

Try the dashboard here: [Sleep Habits & Late-Night Screen Time Dashboard](https://bedtime-data-app-rzqkralqehjquagsinhk4w.streamlit.app/)

## GitHub Repository

Source code and dataset: [bedtime-data-app](https://github.com/lynnetta821/bedtime-data-app)
## Purpose
This Streamlit app helps a health-program or wellness-program manager explore patterns in bedtime phone use, sleep duration, reported sleep debt, and next-day fatigue. It is an exploratory dashboard for prioritizing questions for further investigation, not a diagnostic or causal tool.

## Intended user and decision
**Intended user:** a health or wellness program manager.

**Decision supported:** identify patterns worth exploring in sleep-education materials, such as whether phone-use duration and sleep outcomes vary across groups. The dashboard can support discussion about where to investigate further; it cannot show that phone use causes a particular sleep outcome.

## Data source
- Dataset: [Sleep Debt and Screen Time: Late Night Phone Habits](https://www.kaggle.com/datasets/samartalwar/sleep-debt-and-screen-time-late-night-phone-habits)
- Publisher shown on Kaggle: Samartalwar.
- Data used: the CSV snapshot downloaded for this assignment.
- Each row represents one record/user in the supplied dataset. `user_id` is used as a record identifier.
- The dataset file does not itself establish a real-world collection period or prove that records were collected from actual participants. Check the Kaggle dataset description for any additional provenance details before making stronger claims.

## Main design choices
- **Summary metrics** show the number of records currently in view, average sleep duration, average bedtime phone-use minutes, and the share labelled “Severe Sleep Debt.” These provide a quick overview.
- **Scatter plot** compares bedtime phone-use minutes with total sleep hours and colors points by sleep-debt category. It helps the user inspect patterns and variation rather than assuming a simple cause-and-effect relationship.
- **Box plot** compares sleep-duration distributions across sleep-debt categories, showing medians and spread rather than only averages.
- **Category chart** shows the distribution of sleep-debt labels in the selected records.
- **Bedtime-app chart** compares average sleep hours across reported primary apps, with record counts, phone-use time, and fatigue available on hover.
- **Filters** for age, occupation, sleep-debt category, and blue-light filter let users inspect subsets without creating separate dashboards for each group.
- **Filtered-data table and download** allow the user to review the records behind the displayed patterns.

## Metrics intentionally not emphasized
- **Screen brightness alone:** although it may be interesting, a single brightness percentage is difficult to interpret without knowing device settings and context. It is not included among the headline metrics.
- **Alarm snooze count alone:** this may be influenced by work schedules, alarm habits, and other factors. It is available in the data table but is not given a headline chart because it is less directly tied to the primary question than sleep duration and bedtime phone use.

## Update frequency
The app uses a static CSV file and does not refresh automatically. For this assignment, it displays the downloaded Kaggle snapshot. In a real program, monthly review or refresh could be a starting point if the data provider supplies new data monthly; the actual frequency should follow the source's update schedule and the manager's decision cycle.

## Limitations
- This is an exploratory analysis of the supplied dataset, not medical advice.
- Observed relationships are associations and do not establish causation.
- The CSV alone does not verify the dataset's sampling method, representativeness, or collection dates.
- Small groups can produce unstable averages; users should check record counts before drawing conclusions.

## Run locally
1. Install Python.
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`

## Files
- `app.py`: Streamlit dashboard code.
- `requirements.txt`: Python package dependencies.
- `bedtime_screentime_sleep_debt.csv`: dataset snapshot used by the app.
