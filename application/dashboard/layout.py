html_layout = '''<!DOCTYPE html>
                    <html>
                        <head>
                            {%metas%}
                            <title>{%title%}</title>
                            {%favicon%}
                            {%css%}
                        </head>
                        <body>
                            <nav>
                              <a href="/"><i class="fas fa-home"></i> Home</a>
                              <a href="/dashapp/"><i class="fas fa-chart-line"></i> Data Breach Visualization</a>
                              <a href="/stockdash/"><i class="fas fa-chart-line"></i>Stock Price after Breach</a>
                            </nav>
                            {%app_entry%}
                            <footer>
                                {%config%}
                                {%scripts%}
                                {%renderer%}
                            </footer>
                        </body>
                    </html>'''
