from numex.plugins import EXT

try:
    import nibabel as nib


    def load(filepath, **_kws):
        """
        Load a NiBabel-supported file.

        Args:
            filepath (str): The input file path.
            kws (dict|Iterable): Keyword arguments for `nibabel.load()`.

        Returns:
            arr (np.ndarray): The array data.

        See Also:
            nibabel.load(), nibabel.get_data(), nibabel.get_affine(),
            nibabel.get_header()
        """
        obj = nib.load(filepath, **_kws)
        return obj.get_data()


    EXT['nii'] = load
    EXT['nii.gz'] = load

except ImportError:
    pass
