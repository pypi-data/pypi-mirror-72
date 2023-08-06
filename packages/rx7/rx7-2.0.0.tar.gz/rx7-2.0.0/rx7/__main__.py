import sys
if sys.argv[1] in ('color','colors'): 
    import webbrowser
    webbrowser.open_new_tab(f'{str(__file__)[:-11]}COLORS.html')
if sys.argv[1] in ('-h','--help','help'):
    import webbrowser
    webbrowser.open_new_tab(f'https://pypi.org/project/rx7')