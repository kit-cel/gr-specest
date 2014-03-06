Open issues related to the port to the GNU Radio 3.7 API
--------------------------------------------------------

- welch and welchsp segfault in the destructor. Therefore the unit tests fails, too. 
- MUSIC uses the fortran subroutine music which was not present (only a subroutine called music_spectrum existed). Actually, the whole file looks a lot like work in progress. So I created a dummy fortran file which implements the music method (without doing any real work). A quick test with the specest_gui and the provided sample file produced sensible results, so maybe this isn't even used. Didn't look into this further.
