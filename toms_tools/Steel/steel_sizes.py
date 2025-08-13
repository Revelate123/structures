
class UC200_46:
    def __init__(self):
        self.d=203e-3 
        self.db=203e-3
        self.dt_f=11e-3
        self.dt_w=7.3e-3
        self.dr=11.4e-3
        self.dn_r=10
    
    def __iter__(self):
        return iter((self.d, self.db, self.dt_f, self.dt_w, self.dr, self.dn_r))

class UC150_37:
    def __init__(self):
        self.d=162e-3 
        self.db=154e-3
        self.dt_f=11.5e-3
        self.dt_w=8.1e-3
        self.dr=8.9e-3
        self.dn_r=10
    
    def __iter__(self):
        return iter((self.d, self.db, self.dt_f, self.dt_w, self.dr, self.dn_r))

class UC150_30:
    def __init__(self):
        self.d=158e-3 
        self.db=153e-3
        self.dt_f=9.4e-3
        self.dt_w=6.6e-3
        self.dr=8.9e-3
        self.dn_r=10
    
    def __iter__(self):
        return iter((self.d, self.db, self.dt_f, self.dt_w, self.dr, self.dn_r))
