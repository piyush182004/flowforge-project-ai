import React, { useCallback, useMemo } from 'react';
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { X, Download } from 'lucide-react';

interface WorkflowGraphProps {
  graphData: {
    nodes: any[];
    edges: any[];
    metadata?: any;
  };
  onClose: () => void;
}

const WorkflowGraph: React.FC<WorkflowGraphProps> = ({ graphData, onClose }) => {
  // Convert the graph data to React Flow format
  const initialNodes: Node[] = useMemo(() => {
    return graphData.nodes.map((node) => ({
      id: node.id,
      type: 'default',
      position: node.position,
      data: {
        label: (
          <div className="flex items-center space-x-2">
            {node.icon && <span className="text-lg">{node.icon}</span>}
            <span className="font-medium">{node.label}</span>
          </div>
        ),
        ...node.data,
      },
      style: {
        ...node.style,
        borderRadius: '8px',
        padding: '12px',
        minWidth: '150px',
        textAlign: 'center' as const,
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
      },
    }));
  }, [graphData.nodes]);

  const initialEdges: Edge[] = useMemo(() => {
    return graphData.edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      type: 'smoothstep',
      label: edge.label,
      style: {
        stroke: edge.style?.stroke || '#6B7280',
        strokeWidth: edge.style?.strokeWidth || 2,
        strokeDasharray: edge.style?.strokeDasharray || '0',
      },
      labelStyle: {
        fill: '#6B7280',
        fontWeight: 500,
        fontSize: '12px',
      },
      labelBgStyle: {
        fill: '#1F2937',
        fillOpacity: 0.8,
      },
    }));
  }, [graphData.edges]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const handleDownload = () => {
    const svg = document.querySelector('.react-flow__viewport svg');
    if (svg) {
      const svgData = new XMLSerializer().serializeToString(svg);
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();
      
      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx?.drawImage(img, 0, 0);
        const pngFile = canvas.toDataURL('image/png');
        
        const downloadLink = document.createElement('a');
        downloadLink.download = `workflow-graph-${graphData.metadata?.project_id || 'project'}.png`;
        downloadLink.href = pngFile;
        downloadLink.click();
      };
      
      img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <Card className="w-[90vw] h-[90vh] max-w-7xl">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
          <CardTitle className="text-xl font-bold">
            Workflow Graph
            {graphData.metadata && (
              <span className="text-sm font-normal text-muted-foreground ml-2">
                • {graphData.metadata.total_nodes} nodes, {graphData.metadata.total_edges} edges
              </span>
            )}
          </CardTitle>
          <div className="flex items-center space-x-2">
            <Button variant="outline" size="sm" onClick={handleDownload}>
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
            <Button variant="outline" size="sm" onClick={onClose}>
              <X className="w-4 h-4" />
            </Button>
          </div>
        </CardHeader>
        <CardContent className="h-full p-0">
          <div className="h-full w-full">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              fitView
              attributionPosition="bottom-left"
              className="bg-gradient-to-br from-slate-900 to-slate-800"
            >
              <Controls />
              <Background color="#374151" gap={20} />
              <MiniMap
                nodeColor={(node) => {
                  const nodeData = graphData.nodes.find(n => n.id === node.id);
                  return nodeData?.style?.backgroundColor || '#6B7280';
                }}
                nodeStrokeWidth={3}
                zoomable
                pannable
              />
            </ReactFlow>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default WorkflowGraph; 