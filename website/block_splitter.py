def make_block(obj):
    b = {}
    b['start'] = obj['dep_soll']    
    b['start_loc'] = obj['bp_from']
    b['count'] = obj['reserved']
    b['end'] = obj['arr_soll']
    b['end_loc'] = obj['bp_to']
    return b
    
    
def make_ending_block(obj, prev_end, prev_end_loc):
    b = {}
    b['start'] = prev_end
    b['start_loc'] = prev_end_loc
    b['count'] = obj['reserved']
    b['end'] = obj['arr_soll']
    b['end_loc'] = obj['bp_to']
    return b
    
    
def split_block_start(b,new_obj):
    b1 = {}
    b1['start'] = b['start']
    b1['start_loc'] = b['start_loc']
    b1['count'] = b['count']
    b1['end'] = new_obj['dep_soll']
    b1['end_loc'] = new_obj['bp_from']    
    

    b2 = {}
    b2['start'] = new_obj['dep_soll']
    b2['start_loc'] = new_obj['bp_from']    
    b2['count'] = b['count'] 
    b2['end'] = b['end']
    b2['end_loc'] = b['end_loc']
    
    return b1, b2
    
    
def split_block_end(b,new_obj):
    b1 = {}
    b1['start'] = b['start']
    b1['start_loc'] = b['start_loc']
    b1['count'] = b['count'] + new_obj['reserved']
    b1['end'] = new_obj['arr_soll']
    b1['end_loc'] = new_obj['bp_to']    
    

    b2 = {}
    b2['start'] = new_obj['arr_soll']
    b2['start_loc'] = new_obj['bp_to']    
    b2['count'] = b['count']
    b2['end'] = b['end']
    b2['end_loc'] = b['end_loc']
    
    return b1, b2
    
    
    
# takes a dataframe of reservations for a specific day and specific train_nr
def block_splitter(df):
    blocks = []
    blocks.append(make_block(df.iloc[0]))
    
    curr_block_id = 0
    end = blocks[0]['end']
    
    # go through all rows, sorted by start time
    for row_id in range(1,len(df)):
        row = df.iloc[row_id]
        
        # find block that row[start] fits into
        while curr_block_id < len(blocks) and row['dep_soll'] >= blocks[curr_block_id]['end']:
            curr_block_id += 1
            
            
        # if start goes over the end, just create and add a new block
        if curr_block_id == len(blocks):
            b = make_block(row)
            blocks.append(b)
            end = b['end']
            curr_block_id += 1
            continue
            
        elif row['dep_soll'] == blocks[curr_block_id]['start'] and row['arr_soll'] == blocks[curr_block_id]['end']:
            blocks[curr_block_id]['count'] += row['reserved']
            continue
            
        # else if start is not equal to currents block start, split block up into 2
        elif row['dep_soll'] > blocks[curr_block_id]['start']:
            b1, b2 = split_block_start(blocks[curr_block_id], row)
            del(blocks[curr_block_id])
            blocks.insert(curr_block_id, b1)
            blocks.insert(curr_block_id+1, b2)
            curr_block_id += 1
            
        end_id = curr_block_id
        
        # add count to all blocks in between
        while end_id < len(blocks) and row['arr_soll'] >= blocks[end_id]['end']:
            #if end_id != curr_block_id:
            blocks[end_id]['count'] += row['reserved']
            end_id += 1
            
        
            
        if row['arr_soll'] > end:
            b = make_ending_block(row, end, blocks[-1]['end_loc'])
            blocks.append(b)
            end = row['arr_soll']
        
        elif row['arr_soll'] == end: # end_id == len(blocks):
            continue
        
        elif row['arr_soll'] < blocks[end_id]['end']:
            b1, b2 = split_block_end(blocks[end_id], row)
            del(blocks[end_id])
            blocks.insert(end_id, b1)
            blocks.insert(end_id+1, b2)
             

            
    return blocks
            
            
        
            

            
            
        
        
        