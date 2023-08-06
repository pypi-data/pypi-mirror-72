import unittest
from os.path import abspath, dirname, join, isfile
import os
import numpy as np
import pandas as pd
import json
import matplotlib.pylab as plt
import mhkit.wave as wave
from scipy.interpolate import interp1d
from pandas.testing import assert_frame_equal
import inspect


testdir = dirname(abspath(__file__))
datadir = join(testdir, 'data')

class TestResourceSpectrum(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        omega = np.arange(0.1,3.5,0.01)
        self.f = omega/(2*np.pi)
        self.Hs = 2.5
        self.Tp = 8
        df = self.f[1] - self.f[0]
        Trep = 1/df
        self.t = np.arange(0, Trep, 0.05)
            
    @classmethod
    def tearDownClass(self):
        pass
    
    def test_pierson_moskowitz_spectrum(self):
        S = wave.resource.pierson_moskowitz_spectrum(self.f,self.Tp)
        Tp0 = wave.resource.peak_period(S).iloc[0,0]
        
        error = np.abs(self.Tp - Tp0)/self.Tp
        
        self.assertLess(error, 0.01)
        
    def test_bretschneider_spectrum(self):
        S = wave.resource.bretschneider_spectrum(self.f,self.Tp,self.Hs)
        Hm0 = wave.resource.significant_wave_height(S).iloc[0,0]
        Tp0 = wave.resource.peak_period(S).iloc[0,0]
        
        errorHm0 = np.abs(self.Tp - Tp0)/self.Tp
        errorTp0 = np.abs(self.Hs - Hm0)/self.Hs
        
        self.assertLess(errorHm0, 0.01)
        self.assertLess(errorTp0, 0.01)

    def test_surface_elevation_seed(self):
        S = wave.resource.bretschneider_spectrum(self.f,self.Tp,self.Hs)

        sig = inspect.signature(wave.resource.surface_elevation)
        seednum = sig.parameters['seed'].default
        
        eta0 = wave.resource.surface_elevation(S, self.t)
        eta1 = wave.resource.surface_elevation(S, self.t, seed=seednum)                
        
        assert_frame_equal(eta0, eta1)        

    def test_surface_elevation_phasing(self):
        S = wave.resource.bretschneider_spectrum(self.f,self.Tp,self.Hs)
        eta0 = wave.resource.surface_elevation(S, self.t)        
        sig = inspect.signature(wave.resource.surface_elevation)
        seednum = sig.parameters['seed'].default
        np.random.seed(seednum)
        phases = np.random.rand(len(S)) * 2 * np.pi
        eta1 = wave.resource.surface_elevation(S, self.t, phases=phases)

        assert_frame_equal(eta0, eta1)


    def test_surface_elevation_phases_np_and_pd(self):
        S0 = wave.resource.bretschneider_spectrum(self.f,self.Tp,self.Hs)
        S1 = wave.resource.bretschneider_spectrum(self.f,self.Tp,self.Hs*1.1)
        S = pd.concat([S0, S1], axis=1)

        phases_np = np.random.rand(S.shape[0], S.shape[1]) * 2 * np.pi
        phases_pd = pd.DataFrame(phases_np, index=S.index, columns=S.columns)

        eta_np = wave.resource.surface_elevation(S, self.t, phases=phases_np)
        eta_pd = wave.resource.surface_elevation(S, self.t, phases=phases_pd)

        assert_frame_equal(eta_np, eta_pd)

    def test_surface_elevation_frequency_bins_np_and_pd(self):
        S0 = wave.resource.bretschneider_spectrum(self.f,self.Tp,self.Hs)
        S1 = wave.resource.bretschneider_spectrum(self.f,self.Tp,self.Hs*1.1)
        S = pd.concat([S0, S1], axis=1)

        eta0 = wave.resource.surface_elevation(S, self.t)

        f_bins_np = np.array([np.diff(S.index)[0]]*len(S))
        f_bins_pd = pd.DataFrame(f_bins_np, index=S.index, columns=['df'])

        eta_np = wave.resource.surface_elevation(S, self.t, frequency_bins=f_bins_np)        
        eta_pd = wave.resource.surface_elevation(S, self.t, frequency_bins=f_bins_pd)

        assert_frame_equal(eta0, eta_np)        
        assert_frame_equal(eta_np, eta_pd)        

    def test_surface_elevation_moments(self):
        S = wave.resource.jonswap_spectrum(self.f, self.Tp, self.Hs)
        eta = wave.resource.surface_elevation(S, self.t)
        dt = self.t[1] - self.t[0]
        Sn = wave.resource.elevation_spectrum(eta, 1/dt, len(eta.values), 
                                              detrend=False, window='boxcar',
                                              noverlap=0)

        m0 = wave.resource.frequency_moment(S,0).m0.values[0]
        m0n = wave.resource.frequency_moment(Sn,0).m0.values[0]
        errorm0 = np.abs((m0 - m0n)/m0)

        self.assertLess(errorm0, 0.01)

        m1 = wave.resource.frequency_moment(S,1).m1.values[0]
        m1n = wave.resource.frequency_moment(Sn,1).m1.values[0]
        errorm1 = np.abs((m1 - m1n)/m1)

        self.assertLess(errorm1, 0.01)

    def test_surface_elevation_rmse(self):
        S = wave.resource.jonswap_spectrum(self.f, self.Tp, self.Hs)
        eta = wave.resource.surface_elevation(S, self.t)
        dt = self.t[1] - self.t[0]
        Sn = wave.resource.elevation_spectrum(eta, 1/dt, len(eta), 
                                              detrend=False, window='boxcar',
                                              noverlap=0)

        fSn = interp1d(Sn.index.values, Sn.values, axis=0)
        rmse = (S.values - fSn(S.index.values))**2
        rmse_sum = (np.sum(rmse)/len(rmse))**0.5

        self.assertLess(rmse_sum, 0.02)
    
    def test_jonswap_spectrum(self):
        S = wave.resource.jonswap_spectrum(self.f, self.Tp, self.Hs)
        Hm0 = wave.resource.significant_wave_height(S).iloc[0,0]
        Tp0 = wave.resource.peak_period(S).iloc[0,0]
        
        errorHm0 = np.abs(self.Tp - Tp0)/self.Tp
        errorTp0 = np.abs(self.Hs - Hm0)/self.Hs
        
        self.assertLess(errorHm0, 0.01)
        self.assertLess(errorTp0, 0.01)
    
    def test_plot_spectrum(self):            
        filename = abspath(join(testdir, 'wave_plot_spectrum.png'))
        if isfile(filename):
            os.remove(filename)
        
        S = wave.resource.pierson_moskowitz_spectrum(self.f,self.Tp)
        
        plt.figure()
        wave.graphics.plot_spectrum(S)
        plt.savefig(filename, format='png')
        plt.close()
        
        self.assertTrue(isfile(filename))
        

class TestResourceMetrics(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        file_name = join(datadir, 'ValData1.json')
        with open(file_name, "r") as read_file:
            self.valdata1 = pd.DataFrame(json.load(read_file))
        
        self.valdata2 = {}

        file_name = join(datadir, 'ValData2_MC.json')
        with open(file_name, "r") as read_file:
            data = json.load(read_file)
        self.valdata2['MC'] = data
        for i in data.keys():
            # Calculate elevation spectra
            elevation = pd.DataFrame(data[i]['elevation'])
            elevation.index = elevation.index.astype(float)
            elevation.sort_index(inplace=True)
            sample_rate = data[i]['sample_rate']
            NFFT = data[i]['NFFT']
            self.valdata2['MC'][i]['S'] = wave.resource.elevation_spectrum(elevation, 
                         sample_rate, NFFT)

        file_name = join(datadir, 'ValData2_AH.json')
        with open(file_name, "r") as read_file:
            data = json.load(read_file)
        self.valdata2['AH'] = data
        for i in data.keys():
            # Calculate elevation spectra
            elevation = pd.DataFrame(data[i]['elevation'])
            elevation.index = elevation.index.astype(float)
            elevation.sort_index(inplace=True)
            sample_rate = data[i]['sample_rate']
            NFFT = data[i]['NFFT']
            self.valdata2['AH'][i]['S'] = wave.resource.elevation_spectrum(elevation, 
                         sample_rate, NFFT)
        
        file_name = join(datadir, 'ValData2_CDiP.json')       
        with open(file_name, "r") as read_file:
            data = json.load(read_file)
        self.valdata2['CDiP'] = data
        for i in data.keys():
            temp = pd.Series(data[i]['S']).to_frame('S')
            temp.index = temp.index.astype(float)
            self.valdata2['CDiP'][i]['S'] = temp

            
    @classmethod
    def tearDownClass(self):
        pass

    def test_kfromw(self):
        for i in self.valdata1.columns:
            f = np.array(self.valdata1[i]['w'])/(2*np.pi)
            h = self.valdata1[i]['h']
            rho = self.valdata1[i]['rho']
            
            expected = self.valdata1[i]['k']
            calculated = wave.resource.wave_number(f, h, rho).loc[:,'k'].values
            error = ((expected-calculated)**2).sum() # SSE
            
            self.assertLess(error, 1e-6)
    
    def test_moments(self):
        for file_i in self.valdata2.keys(): # for each file MC, AH, CDiP
            datasets = self.valdata2[file_i]
            for s in datasets.keys(): # for each set
                data = datasets[s]
                for m in data['m'].keys():
                    expected = data['m'][m]
                    S = data['S']
                    if s == 'CDiP1' or s == 'CDiP6':
                        f_bins=pd.Series(data['freqBinWidth'])                       
                    else: 
                        f_bins = None

                    calculated = wave.resource.frequency_moment(S, int(m),frequency_bins=f_bins).iloc[0,0]
                    error = np.abs(expected-calculated)/expected
                    
                    self.assertLess(error, 0.01) 

    

    def test_metrics(self):
       for file_i in self.valdata2.keys(): # for each file MC, AH, CDiP
            datasets = self.valdata2[file_i]
            
            for s in datasets.keys(): # for each set
                
                
                data = datasets[s]
                S = data['S']
                if file_i == 'CDiP':
                    f_bins=pd.Series(data['freqBinWidth'])
                else: 
                    f_bins = None
                
                # Hm0
                expected = data['metrics']['Hm0']
                calculated = wave.resource.significant_wave_height(S,frequency_bins=f_bins).iloc[0,0]
                error = np.abs(expected-calculated)/expected
                #print('Hm0', expected, calculated, error)
                self.assertLess(error, 0.01) 

                # Te
                expected = data['metrics']['Te']
                calculated = wave.resource.energy_period(S,frequency_bins=f_bins).iloc[0,0]
                error = np.abs(expected-calculated)/expected
                #print('Te', expected, calculated, error)
                self.assertLess(error, 0.01) 
                
                # T0
                expected = data['metrics']['T0']
                calculated = wave.resource.average_zero_crossing_period(S,frequency_bins=f_bins).iloc[0,0]
                error = np.abs(expected-calculated)/expected
                #print('T0', expected, calculated, error)
                self.assertLess(error, 0.01) 

                # Tc
                expected = data['metrics']['Tc']
                calculated = wave.resource.average_crest_period(S,frequency_bins=f_bins).iloc[0,0]**2 # Tc = Tavg**2
                error = np.abs(expected-calculated)/expected
                #print('Tc', expected, calculated, error)
                self.assertLess(error, 0.01) 

                # Tm
                expected = np.sqrt(data['metrics']['Tm'])
                calculated = wave.resource.average_wave_period(S,frequency_bins=f_bins).iloc[0,0]
                error = np.abs(expected-calculated)/expected
                #print('Tm', expected, calculated, error)
                self.assertLess(error, 0.01) 
                
                # Tp
                expected = data['metrics']['Tp']
                calculated = wave.resource.peak_period(S).iloc[0,0]
                error = np.abs(expected-calculated)/expected
                #print('Tp', expected, calculated, error)
                self.assertLess(error, 0.001) 
                
                # e
                expected = data['metrics']['e']
                calculated = wave.resource.spectral_bandwidth(S,frequency_bins=f_bins).iloc[0,0]
                error = np.abs(expected-calculated)/expected
                #print('e', expected, calculated, error)
                self.assertLess(error, 0.001) 

                # v
                if file_i == 'CDiP': # this should be updated to run on other datasets
                    expected = data['metrics']['v']                    
                    calculated = wave.resource.spectral_width(S,frequency_bins=f_bins).iloc[0,0]
                    error = np.abs(expected-calculated)/expected

                       
                    self.assertLess(error, 0.01) 

                if file_i == 'MC':
                    expected = data['metrics']['v']
                    calculated = wave.resource.spectral_width(S).iloc[0,0] # testing that default uniform frequency bin widths works 
                    error = np.abs(expected-calculated)/expected

                       
                    self.assertLess(error, 0.01)

                
    def test_plot_elevation_timeseries(self):            
        filename = abspath(join(testdir, 'wave_plot_elevation_timeseries.png'))
        if isfile(filename):
            os.remove(filename)
        
        data = self.valdata2['MC']
        temp = pd.DataFrame(data[list(data.keys())[0]]['elevation'])
        temp.index = temp.index.astype(float)
        temp.sort_index(inplace=True)
        eta = temp.iloc[0:100,:]
        
        plt.figure()
        wave.graphics.plot_elevation_timeseries(eta)
        plt.savefig(filename, format='png')
        plt.close()
        
        self.assertTrue(isfile(filename))
        
class TestPerformance(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        np.random.seed(123)
        Hm0 = np.random.rayleigh(4, 100000)
        Te = np.random.normal(4.5, .8, 100000)
        P = np.random.normal(200, 40, 100000)
        J = np.random.normal(300, 10, 100000)
        
        self.data = pd.DataFrame({'Hm0': Hm0, 'Te': Te, 'P': P,'J': J})
        self.Hm0_bins = np.arange(0,19,0.5)
        self.Te_bins = np.arange(0,9,1)

    @classmethod
    def tearDownClass(self):
        pass
    
    def test_capture_length(self):
        L = wave.performance.capture_length(self.data['P'], self.data['J'])
        L_stats = wave.performance.statistics(L)
        
        self.assertAlmostEqual(L_stats['mean'], 0.6676, 3)
        
    def test_capture_length_matrix(self):
        L = wave.performance.capture_length(self.data['P'], self.data['J'])
        LM = wave.performance.capture_length_matrix(self.data['Hm0'], self.data['Te'], 
                        L, 'std', self.Hm0_bins, self.Te_bins)
        
        self.assertEqual(LM.shape, (38,9))
        self.assertEqual(LM.isna().sum().sum(), 131)
        
    def test_wave_energy_flux_matrix(self):
        JM = wave.performance.wave_energy_flux_matrix(self.data['Hm0'], self.data['Te'], 
                        self.data['J'], 'mean', self.Hm0_bins, self.Te_bins)
        
        self.assertEqual(JM.shape, (38,9))
        self.assertEqual(JM.isna().sum().sum(), 131)
        
    def test_power_matrix(self):
        L = wave.performance.capture_length(self.data['P'], self.data['J'])
        LM = wave.performance.capture_length_matrix(self.data['Hm0'], self.data['Te'], 
                        L, 'mean', self.Hm0_bins, self.Te_bins)
        JM = wave.performance.wave_energy_flux_matrix(self.data['Hm0'], self.data['Te'], 
                        self.data['J'], 'mean', self.Hm0_bins, self.Te_bins)
        PM = wave.performance.power_matrix(LM, JM)
        
        self.assertEqual(PM.shape, (38,9))
        self.assertEqual(PM.isna().sum().sum(), 131)
        
    def test_mean_annual_energy_production(self):
        L = wave.performance.capture_length(self.data['P'], self.data['J'])
        maep = wave.performance.mean_annual_energy_production_timeseries(L, self.data['J'])

        self.assertAlmostEqual(maep, 1754020.077, 2)
    
        
    def test_plot_matrix(self):
        filename = abspath(join(testdir, 'wave_plot_matrix.png'))
        if isfile(filename):
            os.remove(filename)
        
        M = wave.performance.wave_energy_flux_matrix(self.data['Hm0'], self.data['Te'], 
                        self.data['J'], 'mean', self.Hm0_bins, self.Te_bins)
        
        plt.figure()
        wave.graphics.plot_matrix(M)
        plt.savefig(filename, format='png')
        plt.close()
        
        self.assertTrue(isfile(filename))
    
class TestIO(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.expected_columns_metRT = ['WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 
            'APD', 'MWD', 'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'PTDY', 'TIDE']
        self.expected_units_metRT = {'WDIR': 'degT', 'WSPD': 'm/s', 'GST': 'm/s', 
            'WVHT': 'm', 'DPD': 'sec', 'APD': 'sec', 'MWD': 'degT', 'PRES': 'hPa', 
            'ATMP': 'degC', 'WTMP': 'degC', 'DEWP': 'degC', 'VIS': 'nmi', 
            'PTDY': 'hPa', 'TIDE': 'ft'}
        
        self.expected_columns_metH = ['WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 
            'APD', 'MWD', 'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'TIDE']
        self.expected_units_metH = {'WDIR': 'degT', 'WSPD': 'm/s', 'GST': 'm/s', 
            'WVHT': 'm', 'DPD': 'sec', 'APD': 'sec', 'MWD': 'deg', 'PRES': 'hPa', 
            'ATMP': 'degC', 'WTMP': 'degC', 'DEWP': 'degC', 'VIS': 'nmi', 
            'TIDE': 'ft'}
        
    @classmethod
    def tearDownClass(self):
        pass
    
    ### Realtime data
    def test_read_NDBC_realtime_met(self):
        data, units = wave.io.read_NDBC_file(join(datadir, '46097.txt'))
        expected_index0 = pd.datetime(2019,4,2,13,50)
        self.assertSetEqual(set(data.columns), set(self.expected_columns_metRT))
        self.assertEqual(data.index[0], expected_index0)
        self.assertEqual(data.shape, (6490, 14))
        self.assertEqual(units,self.expected_units_metRT)
            
    ### Historical data
    def test_read_NDBC_historical_met(self):
        # QC'd monthly data, Aug 2019
        data, units = wave.io.read_NDBC_file(join(datadir, '46097h201908qc.txt'))
        expected_index0 = pd.datetime(2019,8,1,0,0)
        self.assertSetEqual(set(data.columns), set(self.expected_columns_metH))
        self.assertEqual(data.index[0], expected_index0)
        self.assertEqual(data.shape, (4464, 13))
        self.assertEqual(units,self.expected_units_metH)
        
    ### Spectral data
    def test_read_NDBC_spectral(self):
        data, units = wave.io.read_NDBC_file(join(datadir, 'data.txt'))
        self.assertEqual(data.shape, (743, 47))
        self.assertEqual(units, None)

if __name__ == '__main__':
    unittest.main() 
