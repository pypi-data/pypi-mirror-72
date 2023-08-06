import zipfile
import os

cur_path = os.path.abspath(os.path.dirname(__file__))
log_dir = os.path.join(cur_path, r"../../../")


class ZipConvert:
    def zip_dir(self, dirPath, zipPath):
        zipf = zipfile.ZipFile(zipPath, mode='w')
        lenDirPath = len(dirPath)
        print('Length of Directory %s' % lenDirPath)
        for root, _, files in os.walk(dirPath):
            for file in files:
                filePath = os.path.join(root, file)
                zipf.write(filePath, filePath[lenDirPath:])
                print('Adding File Path to the Zip %s' % filePath)
        zipf.close()

    def unzip_dir(self, path_to_zip_file, directory_to_extract_to):
        if not os.path.exists(directory_to_extract_to):
            print('Directory Doesnt Exist !!!')
            os.makedirs(directory_to_extract_to)
            print('Created Directory !!! %s' % directory_to_extract_to)

        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)
            print('Extracted all the files to %s' % path_to_zip_file)


if __name__ == "__main__":
    zip = ZipConvert()
    zip.zip_dir('%sreport/target' % log_dir,
                '../../../ZIPPPING.zip')
    zip.unzip_dir('%sZIPPPING.zip' % log_dir, '%sunzip' % log_dir)
