import graphviz  # doctest: +NO_EXE
import pandas as pd

# Read data model from excel file
columns_to_read = ['source_gv','dest_gv','node_letter_gv','object_dm','json_tag']
df = pd.read_excel('../data_selection.xlsx', sheet_name='merge', header=0,usecols=columns_to_read)
print(df.head())


# plot Graphviz from dataframe describing overall data model
def make_graph(df):

    # create graphviz nodes
    dot = graphviz.Digraph(name='Data Model Itinéraire',graph_attr={'labelloc':'t','label':'Data Model Itinéraire','fontsize':'24.0','rankdir':'TB'})
    node_letter = df['node_letter_gv']
    object = df['object_dm']
    for letter,obj in zip(node_letter,object):
        dot.node(letter,obj)

    #extract json to be added as a label
    json = df['json_tag']


    #create graphviz relation between nodes
    source = df.loc[1:,'source_gv']
    destination = df.loc[1:,'dest_gv']
    for src,dest,js in zip(source,destination,json):
        dot.edge(src,dest,label=js)


    #Generate Graphiz source code
    print(dot.source)  # doctest: +NORMALIZE_WHITESPACE +NO_EXE

    #Generate Graphiz schema
    dot.render('doctest-output/data_model_itineraire.gv').replace('\\', '/')
    'doctest-output/data_model_itineraire.gv.pdf'

# execute Graph creation
make_graph(df)


