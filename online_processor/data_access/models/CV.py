class CV:
    def __init__(self, photo="", name="", jobTitle="", gender="", age="", birthday="", nativePlace="",
                 phone="", email="", blogs="", nation="", domicilePlace="", currentAddress="",
                 marital="", IDcard="", contactAddress="", highestEducationDegree="", highestEducationBackground="",
                 highestEducationAcademy="", highestEducationMajor="", graduationDate="",
                 startWorkingDate="", workYear="", recentCompany="", recentIndustry="",
                 recentPosition="", currentSalary="", politicsStatus="",
                 expectedOccupation="", expectedSalary="", expectedWorkplace="",
                 expectedCompanyNature="", expectedWorkNature="", expectedIndustry="",
                 expectedStatus="", expectedEntryDate="",
                 selfEvaluation="",
                 educationExperience=[],
                 workExperience=[],
                 projectExperience=[],
                 trainingExperience=[],
                 associationExperience=[],
                 publishPaper=[],
                 publishBook=[],
                 publishPatent=[],
                 skill=[],
                 certificate=[],
                 language=[],
                 award=[],
                 hobby=[],
                 advantage="",
                 _id="", insertTime="", updateTime="", source="", fileFormat="",
                 filePath="", attachmentPath="", plainText="", sameCVid="", md5="", zhilianLabels=[],
                 cv_url="",
                 linked_result="", keyword="", tag=""):
        self.phone = phone
        self.birthday = birthday
        self.age = age
        self.gender = gender
        self.name = name
        self.nativePlace = nativePlace
        self.photo = photo
        self.email = email
        self.blogs = blogs
        self.nation = nation
        self.domicilePlace = domicilePlace
        self.currentAddress = currentAddress
        self.marital = marital
        self.IDcard = IDcard
        self.contactAddress = contactAddress
        self.highestEducationDegree = highestEducationDegree
        self.highestEducationAcademy = highestEducationAcademy
        self.highestEducationMajor = highestEducationMajor
        self.graduationDate = graduationDate
        self.startWorkingDate = startWorkingDate
        self.workYear = workYear
        self.recentCompany = recentCompany
        self.recentIndustry = recentIndustry
        self.recentPosition = recentPosition
        self.currentSalary = currentSalary
        self.politicsStatus = politicsStatus
        self.expectedOccupation = expectedOccupation
        self.expectedSalary = expectedSalary
        self.expectedWorkplace = expectedWorkplace
        self.expectedCompanyNature = expectedCompanyNature
        self.expectedWorkNature = expectedWorkNature
        self.expectedIndustry = expectedIndustry
        self.expectedStatus = expectedStatus
        self.expectedEntryDate = expectedEntryDate
        self.selfEvaluation = selfEvaluation
        self.educationExperience = educationExperience
        self.workExperience = workExperience
        self.projectExperience = projectExperience
        self.trainingExperience = trainingExperience
        self.associationExperience = associationExperience
        self.publishPaper = publishPaper
        self.publishBook = publishBook
        self.publishPatent = publishPatent
        self.skill = skill
        self.certificate = certificate
        self.language = language
        self.award = award
        self.hobby = hobby
        self.advantage = advantage
        self._id = _id
        self.insertTime = insertTime
        self.updateTime = updateTime
        self.source = source
        self.fileFormat = fileFormat
        self.filePath = filePath
        self.attachmentPath = attachmentPath
        self.plainText = plainText
        self.sameCVid = sameCVid
        self.md5 = md5
        self.jobTitle = jobTitle
        self.highestEducationBackground = highestEducationBackground
        self.zhilianLabels = zhilianLabels
        self.cv_url = cv_url
        self.linked_result = linked_result
        self.keyword =keyword
        self.tag = tag

