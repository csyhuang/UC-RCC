def plot_results2(doc_ids,
                 doc_no,
                 target_tag,
                 cosine_scores_text,
                 cosine_scores_tags,
                 jaccard_scores_text,
                 jaccard_scores_tags,
                 statlog,
                 plot_dir,
                 cos_means,
                 jaccard_means):


    ##########################################
    #for item in zip(doc_ids, cosine_scores_text[doc_no], jaccard_scores_text[doc_no], cosine_scores_tags[doc_no],
    #            jaccard_scores_tags[doc_no]):
    #    print("line 185:", item[0], '|',item[1:])
    ##########################################

    print("doc_no:",doc_no)
    doc_key=doc_ids[doc_no]
    print("doc_key:",doc_key)


    # Plot p1
    x1 = range(len(doc_ids))
    y1 = cosine_scores_text[doc_no]

    x2 = range(len(doc_ids))
    #y2 = cosine_scores_tags[doc_no]
    y2 = jaccard_scores_tags[doc_no]

    # Plot p2
    x3 = cosine_scores_text[doc_no]
    y3 = jaccard_scores_text[doc_no]

    # Plot p3
    x4 = doc_ids
    y4 = cosine_scores_text[doc_no]

    #########################################
    # create  plot 1
    #########################################
    a=[]

    index=0

    for item in y1:
        index += 1
        if index != doc_no+1:
            a.append(item)

    stats= "n: " + str(len(a)) + " mean: " + str(statistics.mean(a)) +  ' variance: ' + str(statistics.variance(a))

    statlog.write(','.join([ 'doc-'+str(doc_key), target_tag, str(statistics.mean(a)), str(statistics.variance(a))]))

    cos_means[target_tag].append(statistics.mean(a))

    citation = Label(x=100, y=400, x_units='screen', y_units='screen',
                     text=stats, render_mode='css',
                     border_line_color='black', border_line_alpha=1.0,
                     background_fill_color='white', background_fill_alpha=1.0)

    p1 = figure(title="Cosine Similarity between Doc Index: " + str(doc_no)+' CaseId: '+ str(doc_key) + " and each case tagged with:" + target_tag,
                x_axis_label='Doc Index', y_axis_label='Cosine(Blue)/Jaccard(Red)')

    p1.add_layout(citation)

    p1.circle(x1, y1, color="blue", size=5, legend="text")

    p1.circle(x2, y2, color="red", size=2, legend="tags")

    #########################################
    # create  plot 2
    #########################################

    p2 = figure(title="COS similarity vs Jaccard similarity; CaseId " + str(doc_key), x_axis_label='COS metric', y_axis_label='Jaccard metric')

    p2.circle(x3, y3, color="green")

    #########################################
    # create  plot 3
    #########################################

    a2=[]
    index=0

    for item in y4:
        index += 1
        if index != doc_no+1:
            a2.append(item)

    stats3= "n: " + str(len(a2)) + " mean: " + str(statistics.mean(a2)) +  ' variance: ' + str(statistics.variance(a2))

    statlog.write(',')

    statlog.write(','.join([str(statistics.mean(a2)), str(statistics.variance(a2))]))

    statlog.write('\n')

    jaccard_means[target_tag].append(statistics.mean(a2))

    citation = Label(x=100, y=400, x_units='screen', y_units='screen',
                     text=stats3, render_mode='css',
                     border_line_color='black', border_line_alpha=1.0,
                     background_fill_color='white', background_fill_alpha=1.0)


    p3 = figure(title="Jaccard similarity between Doc Index: " + str(doc_no)+' CaseId: '+ str(doc_key) + " and each case tagged with:" + target_tag,
                x_axis_label='Doc Index', y_axis_label='Jaccard Metric')
    p3.add_layout(citation)

    p3.circle(x4, y4, color="blue")

    ##########################################################################
    # output to HTML file
    ##########################################################################
    output_file(plot_dir+"/cc_cluster_"+target_tag+"_doc_"+str(doc_key)+".html")

    save(row(p1,p2,p3))

    return

