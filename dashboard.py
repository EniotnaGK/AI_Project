import streamlit as st
import pandas as pd
import altair as alt

def intro():
    st.write("# Welcome to Streamlit! 👋")
    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.

        **👈 Select a demo from the dropdown on the left** to see some examples
        of what Streamlit can do!

        ### Want to learn more?

        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community forums](https://discuss.streamlit.io)

        ### See more complex demos

        - Use a neural net to [analyze the Udacity Self-driving Car Image Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )

def data_frame_demo():
    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
    st.write(
        """
        This demo shows how to use `st.write` to visualize Pandas DataFrames.
"""
    )

    @st.cache_data
    def get_data():
        return pd.read_csv("detected_classes.csv")

    try:
        df = get_data()

        # Search bar for image ID
        id_search = st.text_input("Search for an ID")

        if id_search:
            # Filter dataframe by ID
            filtered_df = df[df['id'].astype(str).str.contains(id_search, case=False, na=False)]
            
            # Display images corresponding to filtered IDs
            for image_id in filtered_df['id'].unique():
                image_url = f"C:/Users/antoi/Documents/AI_Project/Recup_images_labellisées/yolo/predict_images/{image_id}"
                st.image(image_url, caption=f"Image ID: {image_id}", use_column_width=True)

            # Display filtered data
            st.write("### Filtered Data", filtered_df)
        else:
            st.warning("Enter an ID to search for images.")

        selected_classes = st.multiselect(
            "Filter by class name",
            options=df['class_name'].unique(),
            default=df['class_name'].unique()
        )
        if selected_classes:
            df = df[df['class_name'].isin(selected_classes)]
        else:
            st.error("Please select at least one class.")

        st.write("### Data", df)

        # Selectbox for choosing the chart type
        chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot"])

        if chart_type == "Bar Chart":
            # Bar Chart
            bar_chart = (
                alt.Chart(df)
                .mark_bar()
                .encode(
                    x='class_name:N',
                    y='count:Q',
                    color='class_name:N',
                    tooltip=['id', 'class_name', 'count']
                )
            )
            st.altair_chart(bar_chart, use_container_width=True)

        elif chart_type == "Line Chart":
            # Line Chart
            line_chart = (
                alt.Chart(df)
                .mark_line()
                .encode(
                    x='id:Q',
                    y='count:Q',
                    color='class_name:N',
                    tooltip=['id', 'class_name', 'count']
                )
            )
            st.altair_chart(line_chart, use_container_width=True)

        elif chart_type == "Scatter Plot":
            # Scatter Plot
            scatter_plot = (
                alt.Chart(df)
                .mark_circle(size=60)
                .encode(
                    x='id:Q',
                    y='count:Q',
                    color='class_name:N',
                    tooltip=['id', 'class_name', 'count']
                )
            )
            st.altair_chart(scatter_plot, use_container_width=True)

    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

page_names_to_funcs = {
    "—": intro,
    "DataFrame Demo": data_frame_demo,
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
