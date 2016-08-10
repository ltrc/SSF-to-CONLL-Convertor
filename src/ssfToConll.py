#!/usr/bin/env python -*- coding: utf-8 -*-

__Author__ = "Riyaz Ahmad Bhat"
__Email__  = "riyaz.ah.bhat@gmail.com"

import os
import re
import sys
import argparse

from collections import namedtuple

from ssfReader import SSFReader


class ConllConvertor (SSFReader):

    def __init__(self, annotation):
        self.annotation = annotation
        #self.check_ = self.treeSanity()
        self.check_ = False #NOTE for raw data
        self.node = namedtuple('node',
                                ('wordForm', 'posTag', 'lemmaFeatures','headType','chunkId','projection',
                                                'depRel','parent','stype','voicetype'))
        self.features = namedtuple('features',
                ('lemma','cat','gen','num','per','case','vib','tam'))

    def convert (self, sentence):
        """                                                                   --- Conll Formatt ---
        1   kAmU    kAmU    n   NNP 
        lex-kAmU|cat-n|gen-m|num-sg|pers-3|case-d|vib-0|tam-0|chunkId-NP|stype-|voicetype-  2   spr _   _
        """
        self.getAnnotations(sentence, self.annotation)

        if self.check_:
            yield "#Error :: "+self.check_
        else:
            for idx, node in enumerate(self.nodeList):
                if node.parent == None and node.depRel == None:
                    head_ = "0"
                    relation_ = "root"
                else:
                    head_ = [str(idy+1) for idy, nodey in enumerate(self.nodeList) \
                            if nodey.headType == node.parent][0]
                    relation_ = node.depRel

                if node.lemmaFeatures.lemma == None:
                    lemma_ = node.wordForm.lower()
                else:
                    lemma_ = node.lemmaFeatures.lemma

                if node.lemmaFeatures.cat in [None,'']:
                    cat_ = node.posTag.lower()
                else:
                    cat_ = node.lemmaFeatures.cat

                if self.annotation == "inter":
                    chunkInfo = node.chunkId
                else:
                    chunkInfo = "%s|chunkType-%s" % (node.chunkId, node.projection)

                features = \
                    "cat-%s|gen-%s|num-%s|pers-%s|case-%s|vib-%s|tam-%s|chunkId-%s|stype-%s|voicetype-%s"\
                    % (node.lemmaFeatures.cat,node.lemmaFeatures.gen,\
                    node.lemmaFeatures.num,node.lemmaFeatures.per,node.lemmaFeatures.case,\
                    node.lemmaFeatures.vib,node.lemmaFeatures.tam,chunkInfo,node.stype,node.voicetype)
                features_ = re.sub("None",'',features)
                yield "\t".join((str(idx+1),node.wordForm,lemma_,cat_,node.posTag,features_,
                            head_,relation_.lower(),"_","_"))

if __name__ == "__main__":

    
    parser = argparse.ArgumentParser(description="SSF to CONLL Convertor!")
    parser.add_argument('--input-file'     , dest='input'     , required=True, help='Input file in ssf format')
    parser.add_argument('--output-file'    , dest='output'    , required=True, help='Output conll file')
    parser.add_argument('--log-file'       , dest='log'       , required=True, help='will contain processing details')
    parser.add_argument('--annotation-type', dest='annotation', required=True, help='annotation type either `inter` or `intra`')
    
    args = parser.parse_args()

    try:
        assert args.annotation in ["intra", "inter"]
    except:
        print "Specify annotation style as either `intra` or `inter`."
        sys.exit()

    if os.path.isfile(os.path.abspath(args.output)):
        outputFile = open(args.output,'a')
    else:
        outputFile = open(args.output,'w')
    
    if os.path.isfile(os.path.abspath(args.log)):
        logFile = open(args.log,'a')
    else:
        logFile = open(args.log,'w')

    with open(args.input) as inputFile: input_ = inputFile.read()
    
    #sentence_ids = re.findall('<Sentence id=(.*?)>', input_)
    sentences = re.finditer("(<Sentence id=.*?>)(.*?)</Sentence>",input_, re.S)
    #sentences = ((for sentence in sentences

    if args.annotation == "inter": allTokens = open('allTokens.txt', 'a')
    filePath = os.path.abspath(args.input)
    logFile.write(filePath+"\n")
    convertor_object = ConllConvertor(args.annotation)
    for sentence in sentences:
        output_ = "\n".join(convertor_object.convert(sentence.group(2).strip()))
        try:
            output_ = "\n".join(convertor_object.convert(sentence.group(2).strip()))
        except Exception, error:
            #logFile.write(filePath+" "+sentence_ids[idx]+" #Error :: Wrong ssf formatt!\n")
            #logFile.write("<Sentence id="+sentence_ids[idx]+">"+" #Error "+str(error)+" :: Wrong ssf formatt!\n")
            logFile.write("%s #Error %s\n" % (sentence.group(1), str(error)))
        else:
            if output_.startswith("#Error"):
                #logFile.write("<Sentence id="+sentence_ids[idx]+">"+" "+output_+"\n")
                logFile.write("%s %s\n" % (sentence.group(1), output_))
            else:
                outputFile.write(output_+"\n\n")
                #logFile.write("<Sentence id="+sentence_ids[idx]+">"+" converted\n")
                logFile.write("%s converted\n" % (sentence.group(1)))

    logFile.close()
    outputFile.close()
    if args.annotation == "inter": allTokens.close()
    if args.annotation == "inter": allTokens.close()
