import os

output_folder = 'weka_files'

class ARFFFile:

    def __init__(self, model_name, selection_name, agg_name, reduce_name, dataset):
        self.model_name = model_name
        self.selection_name = selection_name
        self.agg_name = agg_name
        self.reduce_name = reduce_name
        self.dataset = dataset

    def write_line(self, file, text):
        file.write("{}\n".format(text))

    def write_attributes(self, file):
        num_attributes = len(self.dataset[0]['attributes'])

        for i in range(num_attributes):
            self.write_line(file, "@ATTRIBUTE x{} NUMERIC".format(i))

    def write_class_attribute(self, file):
        class_vals = set()
        for row in self.dataset:
            class_vals.add(row['class_val'])

        self.write_line(file, "@ATTRIBUTE class { " + ",".join(class_vals) + " }")

    def write_data(self, file):
        self.write_line(file, "\n\n@DATA")
        for row in self.dataset:
            attribute_row = ",".join(map(str, row['attributes']))
            self.write_line(file, "{},{}".format(attribute_row, row['class_val']))

    def write_to_file(self):
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        filename = '{}_{}_{}_{}'.format(
            self.model_name, 
            self.selection_name, 
            self.agg_name,
            self.reduce_name)

        with open(os.path.join(output_folder, filename + ".arff"), mode='w') as open_file:
            # Write the relation header
            self.write_line(open_file, "@RELATION {}\n\n".format(filename))

            # Write each attribute
            self.write_attributes(open_file)

            # Write the class attribute
            self.write_class_attribute(open_file)

            # Write the actual data
            self.write_data(open_file)