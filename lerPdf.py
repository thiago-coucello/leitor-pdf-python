import PyPDF4
import io
import csv
import sys

params = sys.argv

if(len(params) < 2):
  file = str(input("Insira o caminho do arquivo a ser processado: "))
else:
  file = params[1]
  
with open(r'{}'.format(file), 'rb') as pdfFileObj:

  pdfReader = PyPDF4.PdfFileReader(pdfFileObj)

  nPages  = pdfReader.getNumPages()

  targets = [
    {"str": "Num AIH", "key": "AIH", "lines": int(0)},
    {"str": "Procedimento principal", "key": "PROC", "lines": int(15)},
    {"str": "Tipo", "key": "TIPO", "lines": int(0)},
    {"str": "Especialidade", "key": "ESPEC", "lines": int(15)}
  ]
  data = [dict() for number in range(nPages)]

  for cont in range(0, nPages):
    pageObj = pdfReader.getPage(cont)
    pagesText = pageObj.extractText()

    if(len(pagesText) < 3000):
      continue

    data[cont]["PAG"] = cont + 1

    for target in targets:
      targetString = target["str"]
      jumpLines = target["lines"]
      key = target["key"]
      saveData = False

      for line in io.StringIO(pagesText):
        if(targetString in line):
          #print("Alvo {} encontrado! Preparando para salvar dados".format(targetString))
          saveData = True
          continue

        #if (key == "PROC" or key == "ESPEC") and cont == 1:
          #print(saveData, jumpLines)

        if(saveData and jumpLines == 0):
          data[cont][key] = line.replace("\n", "")
          saveData = False
          break

        if(saveData and jumpLines > 0):
          jumpLines -= 1

    print(">> Pagina {} foi processada".format(cont))
  filter(None, data)

  with open("resultados.csv", "w") as output:
    example = data[0]
    #print(example.keys())
    handler = csv.DictWriter(output, example.keys())
    output.write("PAGINA, AIH, PROCEDIMENTO PRINCIPAL, TIPO, ESPECIALIDADE\n")
    for line in data:
      if not line:
        continue
      handler.writerow(line)

print("------- # Arquivo {} foi processado # -------".format(file))
    