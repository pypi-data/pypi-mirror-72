import warnings
warnings.filterwarnings("ignore")
#replace can be mm and none. mm= mode for categoric features and median for numeric features
#n_r= null ratio , s_r=skewness ratio , c_r=correalation ratio , n_f=number of features ,t_s= test size, n= remove outliers more than,cat_count= remove categoric columns more than cat_count
def main (train,test,target,Id="None",n_r=0.6,s_r=0.75,c_r=1,n_f="full",t_s=0.25,r_s=42,replace="mm",cat_count=100,n=3,submission="False",cluster="False"):
    import numpy as np # linear algebra
    import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
#-----------------------------------------------------------------------------------------------------------------------------
    if submission=="False":
        dataset=train
    else:
        dataset =  pd.concat(objs=[train, test], axis=0,sort=False).reset_index(drop=True)
#------------------------------------------------------------------------------------------------------------------------------
    #def check_skew(train,target):
     #   if train[target].skew()>=s_r :
      #      train[target]= np.log1p(train[target])

#-----------------------------------------------------------------------------------------------------------------------------
    def drop_na(dataset,target):
        dataset_isna=dataset.isna()
        dataset_isna_sum=dataset_isna.sum()
        dataset_isna_ratio=dataset_isna_sum/len(dataset)
        if target in dataset_isna_ratio:
            dataset_isna_ratio.drop(target,inplace=True)
            remove_columns=dataset_isna_ratio[dataset_isna_ratio>n_r]
        columns=pd.DataFrame(remove_columns)
        #print("2-This Columns will be remove because of null ratio higher than %"+str(n_r*100)+": ")
        #print(remove_columns)
        return columns
    drops=drop_na(dataset,target)
    dataset=dataset.drop(drops.index,axis=1)
#-----------------------------------------------------------------------------------------------------------------------------      
    def replace_null(dataset,replace):
        cat=dataset.select_dtypes("object")   
        fl=dataset.select_dtypes(["float64","int64"]).drop(target,axis=1)
        if replace =="mm":
            for column in cat:
                dataset[column].fillna(dataset[column].mode()[0], inplace=True)
            for column in fl:
                dataset[column].fillna(dataset[column].median(), inplace=True)
        if replace=="none":
            for column in cat:
                dataset[column].fillna("NA", inplace=True)
            for column in fl:
                dataset[column].fillna(0, inplace=True)
    
#-----------------------------------------------------------------------------------------------------------------------------      
    def detect_outliers(dataset,n,features):
        from collections import Counter
        outlier_indices = []
        # iterate over features(columns)
        for col in features:
            # 1st quartile (25%)
            Q1 = np.percentile(dataset[col], 25)
            # 3rd quartile (75%)
            Q3 = np.percentile(dataset[col],75)
            # Interquartile range (IQR)
            IQR = Q3 - Q1
            # outlier step
            outlier_step = 1.5 * IQR 
            # Determine a list of indices of outliers for feature col
            outlier_list_col = dataset[(dataset[col] < Q1 - outlier_step) | (dataset[col] > Q3 + outlier_step )].index
            # append the found outlier indices for col to the list of outlier indices 
            outlier_indices.extend(outlier_list_col)    
        # select observations containing more than 2 outliers
        outlier_indices = Counter(outlier_indices)        
        multiple_outliers = list( k for k, v in outlier_indices.items() if v > n )
        return multiple_outliers 
#-----------------------------------------------------------------------------------------------------------------------------------------------------
    def skew_features(dataset):
        from scipy.special import boxcox1p
        from scipy.stats import boxcox
        from scipy.stats import skew
        lam = 0.15
        #boxcox transform skewed numeric features:
        numeric_feats = dataset.dtypes[dataset.dtypes != "object"].index
        skewed_feats = dataset[numeric_feats].apply(lambda x: skew(x.dropna())) #compute skewness
        skewed_feats = skewed_feats[skewed_feats > s_r]
        skewed_feats = skewed_feats.index
        dataset[skewed_feats] = boxcox1p(dataset[skewed_feats],lam)

#-------------------------------------------------------------------------------------------------------------------------------------
    def clustering(dataset,target):
        from sklearn.metrics import silhouette_score
        from sklearn.cluster import KMeans
        X=dataset[dataset[target].notnull()]._get_numeric_data().drop(target,axis=1)
        y=dataset[target][dataset[target].notnull()]
        km = pd.DataFrame(columns=['cluster',"coef"])
        for n_cluster in range(2, 15):
            kmeans = KMeans(n_clusters=n_cluster,random_state=r_s).fit(X,y)
            label = kmeans.labels_
            sil_coeff = silhouette_score(X, label)
            km = km.append({'cluster': n_cluster,"coef":sil_coeff}, ignore_index=True)
        top_clusters=km.sort_values(by="coef",ascending=False)
        n_c1=top_clusters["cluster"].iloc[0]
        n_c2=top_clusters["cluster"].iloc[1]
        n_c3=top_clusters["cluster"].iloc[3]
        
        new_km1 = KMeans(n_clusters=n_c1, random_state=r_s)
        new1 = dataset._get_numeric_data().dropna(axis=1)
        new_km1.fit(new1)
        predict1=new_km1.predict(new1)
        dataset['cluster1'] = pd.Series(predict1, index=dataset.index)
        
        new_km2 = KMeans(n_clusters=n_c2, random_state=r_s)
        new2 = dataset._get_numeric_data().dropna(axis=1)
        new_km2.fit(new2)
        predict2=new_km2.predict(new2)
        dataset['cluster2'] = pd.Series(predict2, index=dataset.index)
        
        new_km3 = KMeans(n_clusters=n_c3, random_state=r_s)
        new3 = dataset._get_numeric_data().dropna(axis=1)
        new_km3.fit(new3)
        predict3=new_km3.predict(new3)
        dataset['cluster3'] = pd.Series(predict3, index=dataset.index)
        
#------------------------------------------calling functions--------------------------------------------------------------------------------------
    #check_skew(dataset,target)
    drop_na(dataset,target)
    replace_null(dataset,replace)
    if Id=="None":
        features=dataset.select_dtypes(["float64","int64"]).drop([target],axis=1)
    else:
        features=dataset.select_dtypes(["float64","int64"]).drop([target,Id],axis=1)
    dataset_out=dataset[dataset[target].notnull()]
    detect_outliers(dataset_out,n,features)
    Outliers_to_drop = detect_outliers(dataset_out,n,features)
    dataset = dataset.drop(Outliers_to_drop, axis = 0).reset_index(drop=True)
    skew_features(dataset)
    cat=dataset.select_dtypes("object")
    del_col=[]
    for c in cat.columns:
        if len(cat[c].value_counts())>=cat_count:
            del_col.append(c)
    cat=cat.drop(del_col,axis=1)
    dataset=pd.get_dummies(dataset,columns=cat.columns)

    if cluster=="True":
        clustering(dataset,target)
#------------------------------------------train test split--------------------------------------------------------------------------------------    
    if submission=="False":
        train=dataset[dataset[target].notnull()]
    else:
        train=dataset[dataset[target].notnull()]
        test=dataset[dataset[target].isna()]
    
    if n_f=="full":
        k=train.shape[1]
    else:
        k=n_f
    corrmat=abs(dataset.corr())
    cols = corrmat.nlargest(k, target)[target].index
    train_x=train[cols].drop(target,axis=1)
    train_y=train[target]

    if submission=="True":
        X_test=test[cols].drop(target,axis=1)
    
    from sklearn.model_selection import train_test_split
    X_train, X_val, y_train, y_val = train_test_split(train_x, train_y, test_size=t_s, random_state=r_s)
#------------------------------------------all models--------------------------------------------------------------------------------------     
    from sklearn.metrics import confusion_matrix 
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import RobustScaler 
    from sklearn.metrics import mean_squared_error,mean_absolute_error
    from sklearn.ensemble import GradientBoostingClassifier,RandomForestClassifier,AdaBoostClassifier,ExtraTreesClassifier
    from lightgbm import LGBMClassifier
    from catboost import CatBoostClassifier
    from xgboost import XGBClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.gaussian_process import GaussianProcessClassifier
    from sklearn.gaussian_process.kernels import RBF
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.naive_bayes import GaussianNB
    from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
    from sklearn.linear_model import LogisticRegression

    my_models= [ 
               GradientBoostingClassifier(random_state=r_s),
               GradientBoostingClassifier(learning_rate=0.05, n_estimators=120,max_depth=9, min_samples_split=1200,
                                            min_samples_leaf=60, subsample=0.85, max_features=7,random_state=r_s),
               GradientBoostingClassifier(learning_rate=0.01, n_estimators=600,max_depth=9, min_samples_split=1200,
                                            min_samples_leaf=60, subsample=0.85,max_features=7,random_state=r_s),
               GradientBoostingClassifier(learning_rate=0.005, n_estimators=1200,max_depth=9, min_samples_split=1200,
                                            min_samples_leaf=60, subsample=0.85, max_features=7,warm_start=True,random_state=r_s),
               GradientBoostingClassifier(learning_rate=0.005, n_estimators=1500,max_depth=9, min_samples_split=1200, 
                                            min_samples_leaf=60, subsample=0.85, max_features=7,warm_start=True,random_state=r_s),
               RandomForestClassifier(random_state=r_s),
               RandomForestClassifier(n_estimators=200,random_state=r_s),
               RandomForestClassifier(n_estimators=200,min_samples_leaf=3,max_features=0.5,random_state=r_s),
               RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
                                        max_depth=None, max_features='auto', max_leaf_nodes=None,
                                        min_impurity_decrease=0.0, min_impurity_split=None,
                                        min_samples_leaf=1, min_samples_split=2,
                                        min_weight_fraction_leaf=0.0, n_estimators=400, n_jobs=1,
                                        oob_score=False, random_state=r_s, verbose=0,
                                        warm_start=False),
               RandomForestClassifier(n_estimators=50,max_features="sqrt",random_state=r_s),
               AdaBoostClassifier(random_state=r_s),
               ExtraTreesClassifier(random_state=r_s),
               LGBMClassifier(random_state=r_s), 
               CatBoostClassifier(eval_metric='Accuracy',logging_level='Silent',random_state=r_s), 
               XGBClassifier(random_state=r_s),
               XGBClassifier(scale_pos_weight=1,learning_rate=0.01,colsample_bytree = 0.4,subsample = 0.8,
                                objective='binary:logistic',n_estimators=1000,reg_alpha = 0.3,max_depth=4,gamma=10,random_state=r_s),
               XGBClassifier(learning_rate =0.01,n_estimators=5000,max_depth=4,min_child_weight=6,gamma=0,subsample=0.8,
                                colsample_bytree=0.8,reg_alpha=0.005,objective= 'binary:logistic',nthread=4,
                                scale_pos_weight=1,seed=27,random_state=r_s),
               MLPClassifier(random_state=r_s),
               KNeighborsClassifier(3),
               SVC(kernel="linear", C=0.025,random_state=r_s),
               SVC(gamma=2, C=1,random_state=r_s),
               GaussianProcessClassifier(1.0 * RBF(1.0),random_state=r_s),
               DecisionTreeClassifier(random_state=r_s),
               GaussianNB(),
               QuadraticDiscriminantAnalysis(),
               LogisticRegression(random_state=r_s)
               ]
    
    
    scores_val=[]
    scores_train=[]
    MAE=[]
    MSE=[]
    RMSE=[]
    
  
    
    for model in my_models:
        pipe=Pipeline([("scaler",RobustScaler()),("regressor",model)])
        scores_val.append(pipe.fit(X_train,y_train).score(X_val,y_val))
        scores_train.append(pipe.fit(X_train,y_train).score(X_train,y_train))
        y_pred=pipe.predict(X_val)
        MAE.append(mean_absolute_error(y_val,y_pred))
        MSE.append(mean_squared_error(y_val,y_pred))
        RMSE.append(np.sqrt(mean_squared_error(y_val,y_pred)))
        
    results=zip(scores_val,scores_train,MAE,MSE,RMSE)
    results=list(results)
    results_score_val=[item[0] for item in results]
    results_score_train=[item[1] for item in results]
    results_MAE=[item[2] for item in results]
    results_MSE=[item[3] for item in results]
    results_RMSE=[item[4] for item in results]
    df_results=pd.DataFrame({"Algorithm":my_models,"Training Score":results_score_train,"Validation Score":results_score_val,"MAE":results_MAE,"MSE":results_MSE,"RMSE":results_RMSE})
    best_models=df_results.sort_values(by="Validation Score",ascending=False)
    best_model=best_models.iloc[0]
    print(best_model)
    best_model_name=best_models.iloc[0][0]
    print(best_model_name)
    pipe_best=Pipeline([("scaler",RobustScaler()),("regressor",best_model_name)])
    best_model_learn=pipe_best.fit(X_train,y_train)
    y_pred_best=best_model_learn.predict(X_val)
    cm=confusion_matrix(y_val,y_pred_best.round())
    print("Confussion Matrix: ")
    print(cm)
    if submission=="True":
        print(len(X_test))
        prediction=best_model_learn.predict(X_test)
        df_sub = pd.DataFrame()
        df_sub[Id] = test[Id]
        df_sub[target] = prediction.astype(np.int)
        df_sub.to_csv('submission.csv', header=True,index=False)



    






















