-- Story Train Service service
IF NOT EXISTS (SELECT 1 FROM [net].[SysDataSource]
                   WHERE [Name] = 'StoryTrainService')
BEGIN
	  INSERT INTO [net].[SysDataSource]
			   (ID, [Name] ,[StoredProcedureName] ,[ExternalConnectionString] ,[ProviderType] ,[Protocol])
		 VALUES
			   (NEWID(), 'StoryTrainService', '', 'http://tor01t1bld01:5000/UserStory/Prediction/Train', 3, 1)
END

-- Story Prediction Service service
IF NOT EXISTS (SELECT 1 FROM [net].[SysDataSource]
                   WHERE [Name] = 'StoryPredictionService')
BEGIN
	  INSERT INTO [net].[SysDataSource]
			   (ID, [Name] ,[StoredProcedureName] ,[ExternalConnectionString] ,[ProviderType] ,[Protocol])
		 VALUES
			   (NEWID(), 'StoryPredictionService', '', 'http://tor01t1bld01:5000/UserStory/Prediction/Predict', 3, 1)
END
