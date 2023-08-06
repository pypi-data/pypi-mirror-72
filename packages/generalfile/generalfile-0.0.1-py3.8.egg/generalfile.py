from library import *
import csv


class GeneralFile:
    def __init__(self):
        self.backupSuffix = "_BACKUP.txt"
        self.lockSuffix = "_LOCK.txt"

    def scrubDictOfDicts(self, dictOfDicts, indexName):
        """
        dictOfDicts can be singular dict also
        """
        if isinstance(dictOfDicts, dict):
            if isinstance(dictFirstValue(dictOfDicts), dict):
                return dictOfDicts
            else:
                return {dictOfDicts[indexName]: dictOfDicts}

        print(dictOfDicts)
        error("dictOfDicts failed scrubbing, printed above")

    def tsvWrite(self, filepath, dictOfDicts, indexName):
        dictOfDicts = self.scrubDictOfDicts(dictOfDicts, indexName)
        filepath = self.yesTsv(filepath)

        with open(filepath, 'w') as tsvfile:
            writer = csv.writer(tsvfile, delimiter = "\t", lineterminator = "\n")
            writer.writerow(list(dictFirstValue(dictOfDicts, iterate = True).keys()))
            for index, subDict in dictOfDicts.items():
                writer.writerow(list(subDict.values()))
        return dictOfDicts

    def tsvAppend(self, filepath, dictOfDicts, indexName):
        """
        Write instead if file doesn't exist
        """
        filepath = self.yesTsv(filepath)

        if not self.exists(filepath):
            return self.tsvWrite(filepath, dictOfDicts, indexName)

        dictOfDicts = self.scrubDictOfDicts(dictOfDicts, indexName)

        with open(filepath, 'a') as tsvfile:
            writer = csv.writer(tsvfile, delimiter = "\t", lineterminator = "\n")
            for index, subDict in dictOfDicts.items():
                writer.writerow(list(subDict.values()))

        return dictOfDicts

    def tsvRowToDict(self, row):
        return {k: strToDynamicType(v) for k, v in row.items()}

    def tsvRead(self, filepath, indexName):
        """
        Manually add index to each created dict
        Check for indexName duplicates, if there are any just use the last one
        row in reader is an iterator I think, it contains all values as strings, first row will be the labels
        """
        filepath = self.yesTsv(filepath)
        if not self.exists(filepath):
            return {}

        with open(filepath, 'r') as tsvfile:
            reader = csv.DictReader(tsvfile, delimiter = "\t")
            returnDict = {subDict[indexName]: subDict for subDict in map(self.tsvRowToDict, reader)}
            # returnDict = {subDict[indexName]: subDict for subDict in map(dict, reader)}  # Without casting, 3 times faster

        return returnDict

    def yesTsv(self, filepath):
        return "{}.tsv".format(self.noFiletypeEnding(filepath))

    def noFiletypeEnding(self, filepath):
        return filepath.split(".")[0]

    def yesTxt(self, filepath):
        return "{}.txt".format(self.noFiletypeEnding(filepath))

    def yesBackup(self, filepath):
        return "{}{}".format(self.noFiletypeEnding(filepath.replace(self.backupSuffix, "")), self.backupSuffix)

    def checkForOldBackup(self, filepath):
        for i in range(5):
            if self.exists(self.yesBackup(filepath)):
                print("Backup found:", filepath)
                time.sleep(1)
            else:
                return True

        error("Found an old backup file: {}".format(self.yesBackup(filepath)))

    def backupCreate(self, filepath, empty = False):
        if self.exists(filepath):
            self.checkForOldBackup(filepath)
            try:
                if empty:
                    self.write(self.yesBackup(filepath), "backup created from read to prevent misreads from multi-threads")
                else:
                    self.copy(filepath, self.yesBackup(filepath))
            except Exception as e:
                print(e)
                error("Cannot copy file {} -> {}".format(filepath, self.yesBackup(filepath)))
            else:
                return True
        return False

    def backupRemove(self, filepath):
        try:
            self.delete(self.yesBackup(filepath))
        except:
            error("Failed removing backup: {}".format(self.yesBackup(filepath)))

    def exists(self, filepath):
        return os.path.exists(filepath)

    def yesLock(self, filepath):
        return "{}{}".format(self.noFiletypeEnding(filepath.replace(self.lockSuffix, "")), self.lockSuffix)

    def readLock(self, filepath):
        lockFilepath = self.yesLock(filepath)

        try:
            lock = open(lockFilepath, "r")
        except:
            return False
        else:
            try:
                lockPID = int(lock.read())
                lock.close()
            except:
                return False

            return lockPID

    def waitForLock(self, filepath, selfCalls = 0):
        if selfCalls > 10:
            error("waitForLock:selfCalls > 10")

        filepath = self.yesTxt(filepath)
        lockFilepath = self.yesLock(filepath)

        while self.readLock(filepath):
            lockPID = self.readLock(filepath)
            if lockPID == getPID():
                break
            elif lockPID in getPIDs():
                # print("Waiting for lock: {}".format(filepath), lockPID)
                time.sleep(0.01)
            elif not lockPID:
                break
            else:
                # print("Stale lock: {}".format(self.yesLock(filepath)))
                break

        try:
            with open(lockFilepath, "w") as lockFile:
                lockFile.write(str(getPID()))
        except:
            print("Failed creating lock: {}".format(lockFilepath))

        else:

            for i in range(5):
                time.sleep(0.01)
                if self.readLock(filepath) != getPID():
                    break
            else:
                return True

            # print("Lock didn't stick, trying again: {}".format(lockFilepath))

        time.sleep(0.01)
        self.waitForLock(filepath, selfCalls + 1)

    def releaseLock(self, filepath):
        filepath = self.yesTxt(filepath)
        lockFilepath = self.yesLock(filepath)

        lockPID = self.readLock(filepath)
        if lockPID != getPID():
            error("Lock failed: {} - {} != {}".format(lockFilepath, lockPID, getPID()))

        # Maybe we cannot delete because it's being read? I thought it was because it was gone
        for i in range(20):
            try:
                self.delete(lockFilepath)
            except:
                # print("Failed releasing lock #{}: {}".format(i, lockFilepath))
                time.sleep(0.1)
            else:
                return True

        error("Failed releasing lock after certain amount of tries: {}".format(lockFilepath))

    def read(self, filepath, default = None):
        filepath = self.yesTxt(filepath)

        self.waitForLock(filepath)
        createdBackup = self.backupCreate(filepath, empty = True)
        returnObj = default
        try:
            textFile = open(filepath,"r")
        except IOError:
            pass
        else:
            read = textFile.read()
            if read != "":
                try:
                    returnObj = json.loads(read)
                except:
                    print("json.loads failed for {}".format(filepath))
                    returnObj = read
            textFile.close()
        if createdBackup:
            self.backupRemove(filepath)
        self.releaseLock(filepath)
        return returnObj

    def write(self, filepath, serializableObj):
        filepath = self.yesTxt(filepath)

        self.waitForLock(filepath)
        createdBackup = self.backupCreate(filepath)

        textFile = open(filepath, "w")
        jsonDumps = json.dumps(serializableObj)
        textFile.write(jsonDumps)
        textFile.close()

        if createdBackup:
            self.backupRemove(filepath)
        self.releaseLock(filepath)

        return jsonDumps

    def copy(self, filepath, destinationFilepath):
        shutil.copyfile(filepath, destinationFilepath)

    def createFolder(self, dirName):
        if not self.exists(dirName):
            os.mkdir(dirName)

    def clearFolder(self, dirName):
        File().trash(dirName)
        File().createFolder(dirName)

    def trash(self, filepath):
        send2trash(filepath)

    def delete(self, filepath):
        os.remove(filepath)

    def readValue(self, filepath, key):
        values = self.read(filepath, {})
        if key not in values:
            return None
        return values[key]

    def setValue(self, filepath, key, value):
        values = self.read(filepath, {})
        values[key] = value
        self.write(filepath, values)
        return value

    def index(self, filepath, key = None, value = None):
        if value is not None:
            return File().setValue(filepath, key, value)
        else:
            if key is None:
                return File().read(filepath, {})
            else:
                return File().readValue(filepath, key)

    def defaultSuffix(self, filepath, defaultSuffix = ".txt"):
        if "." in filepath:
            return filepath
        return "{}{}".format(filepath, defaultSuffix)

    def getTimeModified(self, filepath):
        filepath = self.defaultSuffix(filepath)
        try:
            return dt.datetime.fromtimestamp(int(os.path.getmtime(filepath)))
        except:
            return None

    def getTimeCreated(self, filepath):
        filepath = self.defaultSuffix(filepath)
        try:
            return dt.datetime.fromtimestamp(int(os.path.getctime(filepath)))
        except:
            return None

class IndexFile:
    def __init__(self, filepath):
        self.filepath = filepath

    def index(self, key = None, value = None):
        return File().index(self.filepath, key, value)



















