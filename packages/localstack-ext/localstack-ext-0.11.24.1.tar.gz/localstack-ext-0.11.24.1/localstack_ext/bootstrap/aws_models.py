from localstack.utils.aws import aws_models
jrwpT=super
jrwpm=None
jrwpC=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  jrwpT(LambdaLayer,self).__init__(arn)
  self.cwd=jrwpm
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,jrwpC,env=jrwpm):
  jrwpT(RDSDatabase,self).__init__(jrwpC,env=env)
 def name(self):
  return self.jrwpC.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
