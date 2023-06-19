import os

class TableGenerator:
    def __init__(self, templateTablePath, templateTableRowPath, pic_dir):
        self.templateTablePath = templateTablePath
        self.templateTableRowPath = templateTableRowPath
        self.pic_dir = pic_dir

    ## Creates a new table with pictures and buttons
    def createPicturesTable(self):
        return self.fillPictureTable()

    ## Fills the table with all pictures in the picture directory
    def fillPictureTable(self):
        rows = ""
        pictures = list(filter(lambda x: x.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')), os.listdir(self.pic_dir)))
        for picture_path in pictures:
            rows += self.fillTableRow(picture_path)
        template = open(self.templateTablePath).read()
        template = template.replace("[PICTURE-ROWS]", rows)
        return template

    ## Fills a table row with the picture and buttons
    def fillTableRow(self, filename: str):
        template = open(self.templateTableRowPath).read()
        template = template.replace("[PICTURE-PATH]", f'{self.pic_dir}/{filename}')
        template = template.replace("[PICTURE-NAME]", filename.split('/')[-1])
        return template