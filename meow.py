"""            if(len(trySplitKeywordparsed) == 3):
                #este es un nombre con apellidos o dos nombres y un apellido
                valorA = trySplitKeywordparsed[0]
                valorB = trySplitKeywordparsed[1]
                valorC = trySplitKeywordparsed[2]

                posibilidad1 = valorA+ " " + valorB + " " + valorC
                posibilidad2 = valorA+ " " + valorC + " " + valorB

                #a = metodoSpacy(posibilidad1,lista)
                #b = metodoSpacy(posibilidad2,lista)

                nombres =  [posibilidad1, posibilidad2] 
                salida = jsonify({'Keyword': keywordparsed, 'Lista': nombres})

                return salida

            if(len(trySplitKeywordparsed) == 4):
                #este es un nombre completo con dos nombres y dos apellidos
                valorA = trySplitKeywordparsed[0]
                valorB = trySplitKeywordparsed[1]
                valorC = trySplitKeywordparsed[1]
                valorD = trySplitKeywordparsed[1]

                posibilidad1 = valorA+ " " +valorB + " " + valorC + " " + valorD
                posibilidad2 = valorA+ " " +valorC + " " + valorB + " " + valorD
                posibilidad3 = valorA+ " " +valorC + " " + valorD + " " + valorB
                posibilidad4 = valorB+ " " +valorA + " " + valorC + " " + valorD
                posibilidad5 = valorB+ " " +valorA + " " + valorD + " " + valorC

                #a = metodoSpacy(posibilidad1,lista)
                #b = metodoSpacy(posibilidad2,lista)
                #c = metodoSpacy(posibilidad3,lista)
                #d = metodoSpacy(posibilidad4,lista)
                #e = metodoSpacy(posibilidad5,lista)

                """