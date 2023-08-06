import matplotlib.pyplot as plt
import seaborn as sns
import spectrum_utils.plot as sup
import spectrum_utils.spectrum as sus
from pyteomics import mgf


plt.style.use(['seaborn-white', 'seaborn-poster'])
plt.rc('font', family='serif')
sns.set_palette('Set1')
# sns.set_context('paper', font_scale=1.3)

spectrum_dict = mgf.get_spectrum(
    '/home/wout/Projects/spectrum_utils/src/docs/spectra.mgf',
    'mzspec:MSV000080679:j11962_C1orf144:scan:10671:DLTDYLMK/2')
identifier = spectrum_dict['params']['title']
precursor_mz = spectrum_dict['params']['pepmass'][0]
precursor_charge = spectrum_dict['params']['charge'][0]
mz = spectrum_dict['m/z array']
intensity = spectrum_dict['intensity array']
retention_time = float(spectrum_dict['params']['rtinseconds'])
peptide = 'WNQLQAFWGTGK'

spectrum_prot = sus.MsmsSpectrum(
    identifier, precursor_mz, precursor_charge, mz, intensity,
    retention_time=retention_time, peptide=peptide)
spectrum_prot.remove_precursor_peak(20, 'ppm').scale_intensity('root').filter_intensity(0.3)
print(spectrum_prot.mz)
print(spectrum_prot.intensity)

sup.colors[None] = '#fefdc4'

fig, ax = plt.subplots(figsize=(4, 2))

sup.spectrum(spectrum_prot, grid=False, ax=ax)

ax.axvline(ax.get_xlim()[0], 0, 1, c='#fefdc4', lw=5)
ax.axhline(0, 0, 1, c='#fefdc4', lw=5)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.xaxis.set_ticks([])
ax.yaxis.set_ticks([])

sns.despine(left=True, bottom=True)

plt.savefig('spec2.png', dpi=300, bbox_inches='tight', transparent=True)
plt.close()

# spectrum_prot.annotate_peptide_fragments(10, 'ppm', 'aby')

# spectrum_dict = mgf.get_spectrum('../../doc/reports/fig/spectra.mgf',
#                                  'CCMSLIB00000840351')
# identifier = spectrum_dict['params']['title']
# precursor_mz = spectrum_dict['params']['pepmass'][0]
# precursor_charge = spectrum_dict['params']['charge'][0]
# mz = spectrum_dict['m/z array']
# intensity = spectrum_dict['intensity array']
#
# spectrum_met = sus.MsmsSpectrum(
#     identifier, precursor_mz, precursor_charge, mz, intensity)
# spectrum_met.filter_intensity(0.05)
#
# charge, tol_mass, tol_mode = 1, 0.5, 'Da'
# annotate_fragment_mz = [133.102, 147.080, 195.117, 237.164, 267.174, 295.170,
#                         313.181, 355.192, 377.172, 391.187, 451.209, 511.231,
#                         573.245, 633.269]
# for fragment_mz in annotate_fragment_mz:
#     spectrum_met.annotate_mz_fragment(fragment_mz, charge,
#                                       tol_mass, tol_mode)
# fragment_smiles = '[H][C@@]1([C@](C2=O)(OC3)C)[C@]4([H])[C@@]([H])(C4(C)C)'\
#                   'C=C[C@@]13C=C5C2=C[C+](C5)C'
# fragment_mz = 295.170
# spectrum_met.annotate_molecule_fragment(fragment_smiles, fragment_mz, charge,
#                                         tol_mass, tol_mode)
#
# fig, axes = plt.subplots(1, 2, figsize=(24, 6))
#
# sup.spectrum(spectrum_prot, grid=False, ax=axes[0])
# axes[0].set_title('WNQLQAFWGTGK/2', fontweight='bold')
#
# sup.spectrum(spectrum_met, grid=False, ax=axes[1])
# axes[1].set_ylim(0, 1.3)
# axes[1].set_title('7,15-O-diacetyl-5-O-benzoyl-3-propanoyl-13,17-oxy-14-'
#                   'oxopremyrsinol', fontweight='bold')
#
# for i, (ax, c) in enumerate(zip(axes, 'AB')):
#     ax.annotate(c, xy=(-0.1, 1.05), xycoords='axes fraction',
#                 fontsize='xx-large', weight='bold')
#
# sns.despine()
#
# plt.savefig('spectrum_utils.pdf', bbox_inches='tight')
# plt.close()
