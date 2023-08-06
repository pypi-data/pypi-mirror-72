from localstack.utils.aws import aws_models
qEwBh=super
qEwBu=None
qEwBF=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  qEwBh(LambdaLayer,self).__init__(arn)
  self.cwd=qEwBu
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,qEwBF,env=qEwBu):
  qEwBh(RDSDatabase,self).__init__(qEwBF,env=env)
 def name(self):
  return self.qEwBF.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
