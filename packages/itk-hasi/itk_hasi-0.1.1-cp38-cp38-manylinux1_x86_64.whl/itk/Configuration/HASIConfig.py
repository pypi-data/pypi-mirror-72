depends = ('ITKPyBase', 'ITKThresholding', 'ITKTestKernel', 'ITKSpatialObjects', 'ITKSmoothing', 'ITKRegistrationCommon', 'ITKRegionGrowing', 'ITKLabelMap', 'ITKImageSources', 'ITKImageGrid', 'ITKDistanceMap', 'ITKConnectedComponents', 'BoneEnhancement', )
templates = (
  ('LandmarkAtlasSegmentationFilter', 'itk::LandmarkAtlasSegmentationFilter', 'itkLandmarkAtlasSegmentationFilterISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('LandmarkAtlasSegmentationFilter', 'itk::LandmarkAtlasSegmentationFilter', 'itkLandmarkAtlasSegmentationFilterIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('LandmarkAtlasSegmentationFilter', 'itk::LandmarkAtlasSegmentationFilter', 'itkLandmarkAtlasSegmentationFilterIUS3IUS3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >'),
  ('LandmarkAtlasSegmentationFilter', 'itk::LandmarkAtlasSegmentationFilter', 'itkLandmarkAtlasSegmentationFilterIF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('LandmarkAtlasSegmentationFilter', 'itk::LandmarkAtlasSegmentationFilter', 'itkLandmarkAtlasSegmentationFilterID3ID3', True, 'itk::Image< double,3 >, itk::Image< double,3 >'),
  ('SegmentBonesInMicroCTFilter', 'itk::SegmentBonesInMicroCTFilter', 'itkSegmentBonesInMicroCTFilterISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('SegmentBonesInMicroCTFilter', 'itk::SegmentBonesInMicroCTFilter', 'itkSegmentBonesInMicroCTFilterISS3IUC3', True, 'itk::Image< signed short,3 >, itk::Image< unsigned char,3 >'),
  ('SegmentBonesInMicroCTFilter', 'itk::SegmentBonesInMicroCTFilter', 'itkSegmentBonesInMicroCTFilterISS3IUS3', True, 'itk::Image< signed short,3 >, itk::Image< unsigned short,3 >'),
)
snake_case_functions = ('landmark_atlas_segmentation_filter', 'segment_bones_in_micro_ct_filter', )
