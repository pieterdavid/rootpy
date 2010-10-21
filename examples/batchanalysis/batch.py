#!/usr/bin/env python

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-v","--verbose", action="store_true", dest="verbose",
                  help="verbose", default=False)
parser.add_option("--nproc", action="store", type="int", dest="nproc",
                  help="number of students", default=1)
parser.add_option("--nevents", action="store", type="int", dest="nevents",
                  help="number of events to process by each student", default=-1)
parser.add_option("--jes", action="store_true", dest="doJESsys",
                  help="recalculate affected variables at EM+JES", default=False)
(options, args) = parser.parse_args()

import sys
import os
import datasets
import ROOT
from TauProcessor import *
from ROOTPy.analysis.batch import Supervisor
from ROOTPy.ntuple import NtupleChain

ROOT.gROOT.ProcessLine('.L dicts.C+')

data = []
for sample in args:
    data += datasets.dataset[sample]

name = "-".join(args)

if options.nproc == 1:
    for dataset in data:
        student = TauProcessor(dataset.files, numEvents = options.nevents, doJESsys=options.doJESsys)
        student.coursework()
        while student.research(): pass
        student.defend()
else:
    supervisor = Supervisor(datasets=data,nstudents=options.nproc,name=name,process=TauProcessor,nevents=options.nevents,verbose=options.verbose,doJESsys=options.doJESsys)
    while supervisor.apply_for_grant():
        supervisor.supervise()
        supervisor.publish()
