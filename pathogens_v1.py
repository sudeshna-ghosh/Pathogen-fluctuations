import argparse, os
import pandas as pd
import glob

def get_arg_parser():
    parser = argparse.ArgumentParser(
        description='write some description here')
    parser.add_argument(
        'input_file',
        type=argparse.FileType('r'),
        help='The file to process', 
        default='final_genefamilies_cpm-names_unstratified.tsv')
    parser.add_argument(
        '--db', '-d',
        type=str,
        help='Database folder location',
        default='./pathogen_database')
    parser.add_argument(
        '--output_file', '-o',
        type=argparse.FileType('w'),
        help='Output filename',
        default='pathogens_output.txt')
    
    return parser

df_list=['Acinetobacter', 'Burkholderia', 'Burkholderia cepacia complex',
       'Salmonella', 'Shigella', 'Enterobacter',
       'Enterobacter cloacae complex', 'Helicobacter', 'Campylobacter',
       'Enterococcus', 'Escherichia', 'Vibrio', 'Morganella', 'Citrobacter',
       'Providencia', 'Clostrioides', 'Klebsiella', 'Proteus', 'Streptococcus',
       'Staphylococcus', 'Stenotrophomonas',
       'Stenotrophomonas maltophilia group', 'Haemophilus', 'Serratia',
       'Giardia', 'Vermamoeba', 'Acanthamoeba', 'Naegleria',
       'Acinetobacter calcoaceticus baumannii complex', 'Pseudomonas',
       'Legionella', 'Mycobacterium', 'Mycobacterium avium complex']

def main():
    parser = get_arg_parser()
    args = parser.parse_args()

    db_folder = args.db
    input_filename= args.input_file
    output_filename = args.output_file
    
    print("loading input file")
    data = pd.read_csv(input_filename, sep='\t', header=0, index_col=0)
    print("loading database")
    db = pd.DataFrame()
    for file in glob.glob(db_folder + '/pathogen_database_part*.tsv'):
        print(f'loading: {file}', end='\r')
        db = db.append(pd.read_csv(file, sep=',', header=0, index_col=0, dtype=str))
#     db = pd.read_csv(db_filename, sep=',', header=0, index_col=0, dtype='object')
    
    data['sample'] = data.index
    data['uniref_number'] = data['sample'].str.split(':').str[0]
    data['uniref'] = data['uniref_number'].str.split('_').str[1]
    data.index = data['uniref']
    data = data.drop([
        'sample', 'uniref_number', 'uniref'
    ], axis=1)

    for i in range(0,33,1):
        DF = pd.DataFrame(columns = [0])
        DF[0] = db.iloc[:,i]  
        DF = DF.dropna()
        DF.index= DF[0]
        DF.drop(DF.columns[len(DF.columns)-1], axis=1, inplace=True)
        DF1 = pd.concat([data, DF], axis=1, join='inner')
        df_sum = DF1.sum()
        df_sum = df_sum.to_frame()
        df_sum = df_sum.rename(columns={0: i})
        #print (i)
        if i == 0:
            table = df_sum        
        elif i >= 1:
            table = pd.concat([table, df_sum], axis=1, join='inner')

    table.columns =  df_list
    table.to_csv(output_filename)

    
if __name__ == "__main__":
    main()
