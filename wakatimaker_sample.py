from wakati_maker import WakatiMaker

wm = WakatiMaker()

categories = "취업", "공지"
job_divisions = "공지", "취업", "인턴십", "교육", "멘토", "행사"
snowe_division = "공지", "모집", "학사", "행사", "학생", "장학", "시스템"
all_divisions = job_divisions, snowe_division

snowe_outfile_names = "snowe_gongji", "snowe_mojip", "snowe_haksa", "snowe_haengsa", "snowe_haksaeng", "snowe_janghak", "snowe_system"
job_outfile_names = "job_gongji", "job_chuiup", "job_internship", "job_gyoyuk", "job_mentor", "job_haengsa"
all_outfile_names = job_outfile_names, snowe_outfile_names
txt = ".txt"
wakati = ".wakati"

for i in range(0, len(categories)):
    category = categories[i]
    print(str(i)+" "+category)
    for j in range(0, len(all_divisions[i])):
        division = all_divisions[i][j]
        outfile_name = all_outfile_names[i][j]
        wm.do_snowe2vec(category, division, "C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/"+outfile_name+txt, outfile_name+wakati)

wm.do_snowe2vec('국제', '국제', "C:/ProgramData/MySQL/MySQL Server 5.7/Uploads/global.txt", "global.wakati")

print("ok")