from IPython.core.display import display, HTML

def wrap_style():
    return {
        "selector": "td", 
        "props": [
            ("max-width", "800px"), 
            ("white-space", "normal"), 
            ("word-wrap", "break-word"),
            ("text-align", "left")
        ]
    }

def header_style():
    return {
        "selector": "th", 
        "props": [
            ("text-align", "left")
        ]
    }

def style_dataframe(df):
    df_no_index = df.copy()
    df_no_index.index = [''] * df_no_index.shape[0]
    
    # Convert newline characters to <br> for proper rendering in HTML for string columns only
    for col in df_no_index.select_dtypes(include=['object']).columns:
        df_no_index[col] = df_no_index[col].apply(lambda x: str(x).replace("\n", "<br>"))
    
    styled_df = df_no_index.style.set_table_styles([wrap_style(), header_style()]).format({"cost": "${:,.3f}"})
    return HTML(styled_df.to_html(escape=False))
  