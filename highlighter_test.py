import fitz

doc = fitz.open("./foo.pdf")
inst_counter = 0
for pi in range(doc.page_count):
    page = doc[pi]

    text = "pagamento"
    text_instances = page.search_for(text)

    for inst in text_instances:
        inst_counter += 1
        highlight = page.add_highlight_annot(inst)

        # define a suitable cropping box which spans the whole page 
        # and adds padding around the highlighted text
      
        zoom_mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=zoom_mat)
        
        
            #pix.save(f"./pg{pi}-hl{inst_counter}.png")
    pix.save("./dsjlhfgkjashjflsdhjflksdjklf.png")
    
doc.close()