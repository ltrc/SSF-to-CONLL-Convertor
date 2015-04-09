How to use?
```
bash ssf2conll.sh <input (file|directory)> <output file> <log file> <annotation type (intra|inter)>
```
The data should be in [Shakti Standard Format (SSF)](http://ltrc.iiit.ac.in/nlptools2010/files/documents/SSF.pdf). Inter-Chunk dependecies should be formated as in the following:
```
<Sentence id='1'>
1       ((      NP      <fs name='NP' drel='k1:VGF'>
1.1     mEM     PRP     <fs af='mEM,pn,any,sg,1,d,0,0' name='mEM' posn='10'>
1.2     wo      RP      <fs af='wo,avy,,,,,,' name='wo' posn='20'>
        ))
2       ((      NP      <fs name='NP2' drel='k1s:VGF'>
2.1     axanA   JJ      <fs af='axanA,adj,m,sg,,d,,' name='axanA' posn='30'>
2.2     sA      RP      <fs af='sA,avy,m,sg,,d,,' name='sA' posn='40'>
2.3     iMsAna  NN      <fs af='iMsAna,n,m,sg,3,d,0,0' name='iMsAna' posn='50'>
        ))
3       ((      VGF     <fs name='VGF' stype='declarative' voicetype='active'>
3.1     hUM     VM      <fs af='hE,v,any,sg,1,,hE,hE' name='hUM' posn='60'>
        ))
4       ((      BLK     <fs name='BLK' drel='rsym:VGF'>
4.1     .       SYM     <fs af='.,punc,,,,,,' name='.' posn='70'>
        ))
</Sentence>
```
While Intra-Chunk dependencies should in the following format:
```
<Sentence id='2'>
1       Kusa    JJ      <fs af='Kusa,adj,any,any,,,,' drel='pof:raha' posn='10' name='Kusa' chunkId='JJP' chunkType='head:JJP'>
2       raha    VM      <fs af='raha,v,any,sg,2,,0,0' stype='declarative' posn='20' voicetype='active' name='raha' chunkId='VGF' chunkType='head:VGF'>
3       XUlIcanxa       NNP     <fs af='XUlIcanxa,n,m,sg,3,d,0,0' drel='rad:raha' posn='30' name='XUlIcanxa' chunkId='NP' chunkType='head:NP'>
4       .       SYM     <fs af='.,punc,,,,,,' drel='rsym:raha' posn='40' name='.' chunkId='BLK' chunkType='head:BLK'>
</Sentence>
```
Output of Sentence 2 in CONLL would look like:
```
1       Kusa    Kusa    adj     JJ      cat-adj|gen-any|num-any|pers-|case-|vib-|tam-|chunkId-JJP|chunkType-head|stype-|voicetype-      2       pof     _       _
2       raha    raha    v       VM      cat-v|gen-any|num-sg|pers-2|case-|vib-0|tam-0|chunkId-VGF|chunkType-head|stype-declarative|voicetype-active     0       main    _       _
3       XUlIcanxa       XUlIcanxa       n       NNP     cat-n|gen-m|num-sg|pers-3|case-d|vib-0|tam-0|chunkId-NP|chunkType-head|stype-|voicetype-        2       rad     _       _
4       .       .       punc    SYM     cat-punc|gen-|num-|pers-|case-|vib-|tam-|chunkId-BLK|chunkType-head|stype-|voicetype-   2       rsym    _       _

```
Following are the dependencies of the convertor:
```
1. headcomputation
2. vibhakticomputation
```
Set the environment variable ssf2conll to the converter directory in ~/.bashrc as:
```
export ssf2conll="/home/usr/SSF-to-CONLL-Convertor"
```
