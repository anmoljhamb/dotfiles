#!/bin/bash

installPreReq(){
  PRE_REQS=$(tr '\n' ' ' < ./pre-reqs.txt)
  sudo apt install $PRE_REQS
}

installPreReq
