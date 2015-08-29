import ncepbufr

hdstr1 ='SAID SIID FOVN YEAR MNTH DAYS HOUR MINU SECO CLAT CLON CLATH CLONH HOLS'
hdstr2 ='SAZA SOZA BEARAZ SOLAZI'

# read amsua radiance file.

bufr = ncepbufr.open('../test/1bamua')
bufr.print_table()
while bufr.advance() == 0:
    print bufr.msg_counter, bufr.msg_type, bufr.msg_date
    while bufr.load_subset() == 0:
        hdr1 = bufr.read_subset(hdstr1)
        hdr2 = bufr.read_subset(hdstr2)
        yyyymmddhhss ='%04i%02i%02i%02i%02i%02i' % tuple(hdr1[3:9])
        # for satellite id, see common code table c-5
        # (http://www.emc.ncep.noaa.gov/mmb/data_processing/common_tbl_c1-c5.htm#c-5)
        # for sensor id, see common code table c-8
        # (http://www.emc.ncep.noaa.gov/mmb/data_processing/common_tbl_c8-c14.htm#c-8)
        print 'sat id,sensor id lat, lon, yyyymmddhhmmss =',int(hdr1[0].item()),\
        int(hdr1[1].item()),hdr1[9].item(),hdr1[10].item(),yyyymmddhhss
        obs = bufr.read_subset('TMBR',pivot=True)
        nchanl = obs.shape[-1]
        for k in xrange(nchanl):
            print 'channel, tb =',k+1,obs[0,k]
    # only loop over first 4 subsets
    if bufr.msg_counter == 4: break
bufr.close()