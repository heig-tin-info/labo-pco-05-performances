CXX      ?= g++
CXXFLAGS ?= -O3 -std=c++17 -Wall

BINARIES = branch-misprediction dram-refresh false-sharing locality-line locality-col

.PHONY: all clean

all: $(BINARIES)

branch-misprediction: branch-misprediction.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

dram-refresh: dram-refresh.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

false-sharing: false-sharing.cpp
	$(CXX) $(CXXFLAGS) -pthread -o $@ $<

locality-line: locality.cpp
	$(CXX) $(CXXFLAGS) -DLINE -o $@ $<

locality-col: locality.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -f $(BINARIES) *.dat *.csv
