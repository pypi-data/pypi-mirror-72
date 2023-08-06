from localstack.utils.aws import aws_models
AvFuw=super
AvFuf=None
AvFup=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  AvFuw(LambdaLayer,self).__init__(arn)
  self.cwd=AvFuf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,AvFup,env=AvFuf):
  AvFuw(RDSDatabase,self).__init__(AvFup,env=env)
 def name(self):
  return self.AvFup.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
